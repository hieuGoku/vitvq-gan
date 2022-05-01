# ------------------------------------------------------------------------------------
# Enhancing Transformers
# Copyright (c) 2022 Thuan H. Nguyen. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 [see LICENSE for details]
# ------------------------------------------------------------------------------------
# Modified from DALLE-pytorch (https://github.com/lucidrains/DALLE-pytorch)
# Copyright (c) 2020 Phil Wang. All Rights Reserved.
# ------------------------------------------------------------------------------------

from typing import Optional, Union, Callable, Tuple, Any
from pathlib import Path
from omegaconf import OmegaConf
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torch.utils.data import Dataset

from ..utils.general import initialize_from_config

class CC3MBase(Dataset):
    def __init__(self, folder: str, split: str,
                 tokenizer: OmegaConf,
                 transform: Callable) -> None:
        super().__init__()

        for line in open(f'{Path(folder)}/{split}_list.txt', 'r').readlines():
            imgpath, text = line.strip().split('\t')
            self.items.append((Path(folder)/imgpath, text))

        self.tokenizer = initialize_from_config(tokenizer)
        self.transform = transform

    def __len__(self) -> int:
        return len(self.keys)

    def __getitem__(self, ind: int) -> Tuple[Any, Any]:
        image_file, caption = self.items[ind]
                
        caption = self.tokenizer.tokenize(caption).squeeze(0)

        image = Image.open(image_file).convert('RGB')
        if self.transform:
            image = self.transform(image)

        # Success
        return {"caption": caption, "image": image}


class CC3MTrain(TextImageBase):
    def __init__(self, folder: str, tokenizer: OmegaConf,
                 resolution: Union[Tuple[int, int], int] = 256) -> None:
        if isinstance(resolution, int):
            resolution = [resolution, resolution]

        transform = albumentations.Compose([
            A.SmallestMaxSize(max_size=min(resolution)),
            A.RandomCrop(height=resolution[0], width=resolution[1]),
            ToTensorV2(),
        ])
        
        super().__init__(folder, 'train', tokenizer, transform)


class CC3MValidation(TextImageBase):
    def __init__(self, folder: str, tokenizer: OmegaConf,
                 resolution: Union[Tuple[int, int], int] = 256) -> None:
        if isinstance(resolution, int):
            resolution = [resolution, resolution]

        transform = albumentations.Compose([
            A.SmallestMaxSize(max_size=min(resolution)),
            A.CenterCrop(height=resolution[0], width=resolution[1]),
            ToTensorV2(),
        ])
        
        super().__init__(folder, 'val', tokenizer, transform)
