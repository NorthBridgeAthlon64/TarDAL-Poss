import logging
import socket
import sys
import warnings
from pathlib import Path
import cv2
import numpy as np
import torch
import torch.hub
from kornia import image_to_tensor, tensor_to_image
from torchvision.transforms import Resize, Compose, Normalize
from tqdm import tqdm

from module.saliency.u2net import U2NETP


def _cv2_imread_unicode(path: str | Path, flags: int):
    """避免从 loader 导入：loader 包初始化会经 checker 再导入本模块，导致循环依赖。"""
    p = Path(path)
    with p.open('rb') as f:
        buf = np.frombuffer(f.read(), dtype=np.uint8)
    if buf.size == 0:
        return None
    return cv2.imdecode(buf, flags)


def _cv2_imwrite_unicode(path: str | Path, img: np.ndarray) -> bool:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if img.dtype != np.uint8:
        img = np.clip(np.asarray(img), 0, 255).astype(np.uint8)
    suf = p.suffix.lower()
    if suf in ('.jpg', '.jpeg'):
        ext = '.jpg'
    elif suf == '.png':
        ext = '.png'
    elif suf == '.bmp':
        ext = '.bmp'
    else:
        ext = '.png'
    ok, buf = cv2.imencode(ext, img)
    if not ok or buf is None:
        return False
    with p.open('wb') as f:
        f.write(buf.tobytes())
    return True


class Saliency:
    r"""
    Init saliency detection pipeline to generate mask from infrared images.
    """

    def __init__(self, url: str):
        # init device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logging.info(f'deploy u2net on device {str(device)}')
        self.device = device

        # init u2net small (u2netp)
        net = U2NETP(in_ch=1, out_ch=1)
        logging.info(f'init u2net small model with (1 -> 1)')
        self.net = net

        # 预训练权重：http(s) 从官方下载；否则视为本地路径（相对当前工作目录或绝对路径）
        ckpt_dir = Path.cwd() / 'weights' / 'v1'
        ckpt_dir.mkdir(parents=True, exist_ok=True)
        ckpt_p = ckpt_dir / 'u2netp.pth'
        socket.setdefaulttimeout(5)
        if isinstance(url, str) and (url.startswith('http://') or url.startswith('https://')):
            logging.info(f'download pretrained u2net weights from {url}')
            try:
                ckpt = torch.hub.load_state_dict_from_url(url, model_dir=ckpt_dir, map_location='cpu')
            except Exception as err:
                logging.fatal(f'load {url} failed: {err}, place mask-u2.pth locally and set saliency url to its path')
                sys.exit(1)
            net.load_state_dict(ckpt)
            logging.info(f'load pretrained u2net weights from hub cache under {ckpt_dir}')
        else:
            local_path = Path(url)
            if not local_path.is_absolute():
                local_path = (Path.cwd() / local_path).resolve()
            if not local_path.is_file():
                logging.fatal(f'local saliency weight not found: {local_path}')
                sys.exit(1)
            logging.info(f'load pretrained u2net weights from local file {local_path}')
            ckpt = torch.load(local_path, map_location='cpu')
            net.load_state_dict(ckpt)

        # move to device
        net.to(device)

        # more parameters
        self.transform_fn = Compose([Resize(size=(320, 320)), Normalize(mean=0.485, std=0.229)])

    @torch.inference_mode()
    def inference(self, src: str | Path, dst: str | Path):
        # create save folder
        dst = Path(dst)
        dst.mkdir(parents=True, exist_ok=True)
        logging.debug(f'create save folder {str(dst)}')

        # forward
        self.net.eval()
        warnings.filterwarnings(action='ignore', lineno=780)
        img_list = sorted(Path(src).rglob('*.png'))
        logging.info(f'load {len(img_list)} images from {str(src)}')
        process = tqdm(img_list)
        for img_p in process:
            process.set_description(f'generate mask for {img_p.name} to {str(dst)}')
            img = self._imread(img_p).to(self.device)
            reverse_fn = Resize(size=img.shape[-2:])
            img = self.transform_fn(img)
            mask = self.net(img.unsqueeze(0))[0]
            mask = (mask - mask.min()) / (mask.max() - mask.min())
            mask = reverse_fn(mask).squeeze()
            _cv2_imwrite_unicode(dst / img_p.name, tensor_to_image(mask) * 255)

    @torch.inference_mode()
    def inference_single(self, ir_tensor: torch.Tensor) -> np.ndarray:
        """
        对单张红外图做显著性检测，得到人体/前景轮廓单通道图（背景黑、前景亮）。
        ir_tensor: [1, H, W] 或 [H, W]，值域 [0, 1]
        返回: [H, W] uint8，0=背景黑，255=前景/人体轮廓
        """
        self.net.eval()
        if ir_tensor.dim() == 2:
            ir_tensor = ir_tensor.unsqueeze(0)
        if ir_tensor.dim() == 3 and ir_tensor.shape[0] != 1:
            ir_tensor = ir_tensor.unsqueeze(0)
        orig_shape = ir_tensor.shape[-2:]
        x = self.transform_fn(ir_tensor).to(self.device)
        mask = self.net(x.unsqueeze(0))[0]
        mask = (mask - mask.min()) / (mask.max() - mask.min() + 1e-8)
        reverse_fn = Resize(size=orig_shape)
        mask = reverse_fn(mask.squeeze(0).cpu()).squeeze()
        return (mask.numpy() * 255).astype(np.uint8)

    @staticmethod
    def _imread(img_p: str | Path):
        img = _cv2_imread_unicode(img_p, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f'cannot read image: {img_p}')
        img = image_to_tensor(img).float() / 255
        return img
