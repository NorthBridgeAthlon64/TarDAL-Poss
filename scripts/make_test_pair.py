"""生成用于 API 测试的最小 IR/VI 图像对（项目内一次性脚本）。"""
import numpy as np
import cv2
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "backend" / "_test_assets"
p.mkdir(parents=True, exist_ok=True)
h, w = 256, 256
ir = np.random.randint(0, 255, (h, w), dtype=np.uint8)
vi = np.zeros((h, w, 3), dtype=np.uint8)
x = np.linspace(0, 255, w, dtype=np.uint8)
vi[:, :, 0] = x
vi[:, :, 1] = 128
vi[:, :, 2] = 255 - x
cv2.imwrite(str(p / "test_ir.png"), ir)
cv2.imwrite(str(p / "test_vi.png"), vi)
print(p)
