import pygame


class Spritesheet:
    def __init__(self, path) -> None:
        self.spritesheet = pygame.image.load(path).convert_alpha()

    def get_sprite(self, x, y, w, h):
        sprite = self.spritesheet.subsurface(pygame.Rect(x, y, w, h))
        return sprite
