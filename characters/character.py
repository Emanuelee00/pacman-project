import pygame
import os
from typing import Optional
from settings import Tile, Directions, SPEED, WALL_SIZE, FLOOR_SIZE, TOLERANCE, CELL_SIZE
from pathlib import Path
from abc import ABC, abstractmethod

class Character(pygame.sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()
        self.walk_anim = []

    SIZE = (40, 40)

    def load_anim(self, folder: str, image_name: Optional[str] = None):
        current_dir = Path(__file__).parent
        assets_dir = current_dir.parent / "assets" / folder
        self.walk_anim = []
        if assets_dir.exists():
            if image_name:
                img = pygame.image.load(assets_dir / image_name)
                img = pygame.transform.scale(img, self.SIZE)
                self.walk_anim.append(img)
            else:
                for file in assets_dir.iterdir():
                    img = pygame.image.load(assets_dir / file)
                    img = pygame.transform.scale(img, self.SIZE)
                    self.walk_anim.append(img)
        return self.walk_anim

    @abstractmethod
    def respawn(self, maze):
        pass
