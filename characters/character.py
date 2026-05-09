import pygame
import os
from typing import Optional
from settings import Tile, Directions, SPEED, WALL_SIZE, FLOOR_SIZE, TOLERANCE, CELL_SIZE
from importlib.resources import files, as_file


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walk_anim = []

    SIZE = (40, 40)

    def load_anim(self, folder: str, image_name: Optional[str] = None):
        assets = files(__package__).joinpath("..", "assets", folder)
        self.walk_anim = []
        if assets:
            if image_name:
                with as_file(assets.joinpath(image_name)) as path:
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img, self.SIZE)
                    self.walk_anim.append(img)
            else:
                for file in assets.iterdir():
                    with as_file(file) as path:
                        img = pygame.image.load(path)
                        img = pygame.transform.scale(img, self.SIZE)
                        self.walk_anim.append(img)
        return self.walk_anim

    @staticmethod
    def _get_dir(*args: str):
        try:
            dir = os.listdir(os.path.join(*args))
            for file in dir:
                if not file.endswith(".png"):
                    raise ValueError
            return dir
        except (FileNotFoundError, ValueError, TypeError) as e:
            print(e)
            return []

    def respawn(self):
        pass
