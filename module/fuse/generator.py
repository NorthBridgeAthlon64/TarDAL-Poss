import torch
import torch.nn as nn
from torch import Tensor


class Generator(nn.Module):
    r"""
    Use to generate fused images.
    ir + vi -> fus
    """

    def __init__(self, dim: int = 32, depth: int = 3):
        super(Generator, self).__init__()
        self.depth = depth

        self.encoder = nn.Sequential(
            nn.Conv2d(2, dim, (3, 3), (1, 1), 1),
            nn.BatchNorm2d(dim),
            nn.ReLU()
        )

        self.dense = nn.ModuleList([
            nn.Sequential(
                nn.Conv2d(dim * (i + 1), dim, (3, 3), (1, 1), 1),
                nn.BatchNorm2d(dim),
                nn.ReLU()
            ) for i in range(depth)
        ])

        self.fuse = nn.Sequential(
            nn.Sequential(
                nn.Conv2d(dim * (depth + 1), dim * 4, (3, 3), (1, 1), 1),
                nn.ReLU()
            ),
            nn.Sequential(
                nn.Conv2d(dim * 4, dim * 2, (3, 3), (1, 1), 1),
                nn.BatchNorm2d(dim * 2),
                nn.ReLU()
            ),
            nn.Sequential(
                nn.Conv2d(dim * 2, dim, (3, 3), (1, 1), 1),
                nn.BatchNorm2d(dim),
                nn.ReLU()
            ),
            nn.Sequential(
                nn.Conv2d(dim, 1, (3, 3), (1, 1), 1),
                nn.Tanh()
            ),
        )

    def forward(self, ir: Tensor, vi: Tensor, return_intermediate: bool = False) -> Tensor | tuple[Tensor, Tensor]:
        src = torch.cat([ir, vi], dim=1)
        x = self.encoder(src)
        for i in range(self.depth):
            t = self.dense[i](x)
            x = torch.cat([x, t], dim=1)
        
        # 获取fuse模块的中间结果
        # fuse模块有4个Sequential层，我们取第三个层的输出作为初步融合结果
        fuse_input = x
        intermediate = self.fuse[0](fuse_input)  # 第一个层
        intermediate = self.fuse[1](intermediate)  # 第二个层
        intermediate = self.fuse[2](intermediate)  # 第三个层 - 作为初步融合结果
        fus = self.fuse[3](intermediate)  # 第四个层 - 最终融合结果
        
        if return_intermediate:
            return fus, intermediate
        return fus
