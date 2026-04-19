from pathlib import Path
from typing import Tuple

import cv2
import numpy
import torch
from kornia import image_to_tensor, tensor_to_image
from kornia.color import rgb_to_ycbcr, bgr_to_rgb, rgb_to_bgr
from torch import Tensor
from torchvision.ops import box_convert


def imread_unicode(path: str | Path, flags: int = cv2.IMREAD_COLOR):
    """
    替代 cv2.imread：在 Windows 下对含中文等非 ASCII 的路径仍可解码图像。
    """
    p = Path(path)
    with p.open('rb') as f:
        buf = numpy.frombuffer(f.read(), dtype=numpy.uint8)
    if buf.size == 0:
        return None
    return cv2.imdecode(buf, flags)


def imwrite_unicode(path: str | Path, img: numpy.ndarray) -> bool:
    """
    替代 cv2.imwrite：支持保存到含中文的路径。
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if img.dtype != numpy.uint8:
        img = numpy.clip(numpy.asarray(img), 0, 255).astype(numpy.uint8)
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


def gray_read(img_path: str | Path) -> Tensor:
    img_n = imread_unicode(img_path, cv2.IMREAD_GRAYSCALE)
    if img_n is None:
        raise FileNotFoundError(f'无法读取图像（路径或编码问题）: {img_path}')
    img_t = image_to_tensor(img_n).float() / 255
    return img_t


def ycbcr_read(img_path: str | Path) -> Tuple[Tensor, Tensor]:
    img_n = imread_unicode(img_path, cv2.IMREAD_COLOR)
    if img_n is None:
        raise FileNotFoundError(f'无法读取图像（路径或编码问题）: {img_path}')
    img_t = image_to_tensor(img_n).float() / 255
    img_t = rgb_to_ycbcr(bgr_to_rgb(img_t))
    y, cbcr = torch.split(img_t, [1, 2], dim=0)
    return y, cbcr


def label_read(label_path: str | Path) -> Tensor:
    target = numpy.loadtxt(str(label_path), dtype=numpy.float32)
    labels = torch.from_numpy(target).view(-1, 5)  # (cls, cx, cy, w, h)
    labels[:, 1:] = box_convert(labels[:, 1:], 'cxcywh', 'xyxy')  # (cls, x1, y1, x2, y2)
    return labels


def img_write(img_t: Tensor, img_path: str | Path):
    if img_t.shape[0] == 3:
        img_t = rgb_to_bgr(img_t)
    img_n = tensor_to_image(img_t.squeeze().cpu()) * 255
    if not imwrite_unicode(img_path, img_n):
        raise OSError(f'无法保存图像: {img_path}')


def label_write(pred_i: Tensor, txt_path: str | Path):
    for *pos, conf, cls in pred_i.tolist():
        line = (cls, *pos, conf)
        with txt_path.open('a') as f:
            f.write(('%g ' * len(line)).rstrip() % line + '\n')
