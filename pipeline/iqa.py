import logging
import socket
import sys
from pathlib import Path
from typing import Literal

import cv2
import torch.cuda
from kornia import image_to_tensor, tensor_to_image
from torch import Tensor
from torchvision.models import vgg16
from torchvision.transforms import Compose, Resize, Normalize
from tqdm import tqdm


class IQA:
    r"""
    Init information measurement pipeline to generate iqa from source images.
    """

    def __init__(self, url: str):
        # init device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logging.info(f'deploy iqa on device {str(device)}')
        self.device = device

        # init vgg backbone
        extractor = vgg16().features
        logging.info(f'init iqa extractor with (3 -> 1)')
        self.extractor = extractor

        ckpt_dir = Path.cwd() / 'weights' / 'v1'
        ckpt_dir.mkdir(parents=True, exist_ok=True)
        ckpt_p = ckpt_dir / 'iqa.pth'
        socket.setdefaulttimeout(5)
        if isinstance(url, str) and (url.startswith('http://') or url.startswith('https://')):
            logging.info(f'download pretrained iqa weights from {url}')
            try:
                ckpt = torch.hub.load_state_dict_from_url(url, model_dir=ckpt_dir, map_location='cpu')
            except Exception as err:
                logging.fatal(f'load {url} failed: {err}, place iqa-vgg.pth locally and set iqa url to its path')
                sys.exit(1)
            extractor.load_state_dict(ckpt)
            logging.info(f'load pretrained iqa weights from hub cache under {ckpt_dir}')
        else:
            local_path = Path(url)
            if not local_path.is_absolute():
                local_path = (Path.cwd() / local_path).resolve()
            if not local_path.is_file():
                logging.fatal(f'local iqa weight not found: {local_path}')
                sys.exit(1)
            logging.info(f'load pretrained iqa weights from local file {local_path}')
            ckpt = torch.load(local_path, map_location='cpu')
            extractor.load_state_dict(ckpt)

        # move to device
        extractor.to(device)

        # more parameters
        self.transform_fn = Compose([Resize((672, 672)), Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
        self.upsample = Resize((672, 672))

    @torch.inference_mode()
    def inference(self, src: str | Path, dst: str | Path):
        self.modality_inference(src, dst, 'ir')
        self.modality_inference(src, dst, 'vi')

    @torch.inference_mode()
    def modality_inference(self, src: str | Path, dst: str | Path, modality: Literal['ir', 'vi']):
        # create save folder
        dst = Path(dst / modality)
        dst.mkdir(parents=True, exist_ok=True)
        logging.debug(f'create save folder {str(dst)}')

        # forward
        self.extractor.eval()
        img_list = sorted(Path(src / modality).rglob('*.png'))
        logging.info(f'load {len(img_list)} images from {str(src)}')
        process = tqdm(img_list)
        for img_p in process:
            process.set_description(f'generate iqa for {img_p.name} to {str(dst)}')
            img = self._imread(img_p).to(self.device)
            reverse_fn = Resize(size=img.shape[-2:])
            iqa = self.extractor_inference(img.unsqueeze(0))[0]
            iqa = reverse_fn(iqa).squeeze()
            cv2.imwrite(str(dst / img_p.name), tensor_to_image(iqa) * 255)

    @torch.inference_mode()
    def extractor_inference(self, x: Tensor) -> Tensor:
        # information measurement
        l_ids = [3, 8, 15, 22, 29]  # layers before max-pooling
        f = []
        x = x.repeat(1, 3, 1, 1) if x.size(dim=1) == 1 else x
        x = self.transform_fn(x)
        for index, layer in enumerate(self.extractor):
            x = layer(x)
            if index in l_ids:
                t = x.mean(axis=1, keepdims=True)
                f.append(self.upsample(t))
        f = torch.cat(f, dim=1).mean(axis=1, keepdims=True)
        return f

    @staticmethod
    def _imread(img_p: str | Path):
        img = cv2.imread(str(img_p), cv2.IMREAD_GRAYSCALE)
        img = image_to_tensor(img).float() / 255
        return img
