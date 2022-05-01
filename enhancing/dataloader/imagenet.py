# ------------------------------------------------------------------------------------
# Enhancing Transformers
# Copyright (c) 2022 Thuan H. Nguyen. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 [see LICENSE for details]
# ------------------------------------------------------------------------------------

import PIL
from typing import Any, Tuple, Union
import albumentations as A
from albumentations.pytorch import ToTensorV2

import torch
from torchvision.datasets import ImageNet


class ImageNetBase(ImageNet):
    def __init__(self, root: str, split: str,
                 transform: Optional[Callable] = None) -> None:
        super().__init__(root=root, split='train', transform=transform)
        
    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        sample, target = super().__getitem__(index)

        return {'image': sample, 'class': target.unsqueeze(-1)}


class ImageNetTrain(ImageNetBase):
    def __init__(self, root: str, resolution: Union[Tuple[int, int], int] = 256) -> None:
        if isinstance(resolution, int):
            resolution = [resolution, resolution]

        transform = A.Compose([
            A.SmallestMaxSize(max_size=min(resolution)),
            A.RandomCrop(height=resolution[0], width=resolution[1]),
            A.RandomHorizontalFlip(),
            ToTensorV2()
        ])
        
        super().__init__(root=root, split='train', transform)
        

class ImageNetValidation(ImageNetBase):
    def __init__(self, root: str, resolution: Union[Tuple[int, int], int] = 256) -> None:
        if isinstance(resolution, int):
            resolution = [resolution, resolution]

        transform = A.Compose([
            A.SmallestMaxSize(max_size=min(resolution)),
            A.CenterCrop(height=resolution[0], width=resolution[1]),
            ToTensorV2()
        ])
        
        super().__init__(root=root, split='val', transform)
