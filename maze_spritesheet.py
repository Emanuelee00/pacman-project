import pygame


class MazeSpritesheet:
    def __init__(self, spritesheet):
        self.spritesheet = spritesheet

    def get_sprite(self, x, y, width, height):
        return self.spritesheet.subsurface(pygame.Rect(x, y, width, height))


Tiles = {
    1: (0, 0, 24, 24),
    2: (24, 0, 24, 24),
    3: (48, 0, 24, 24),
    4: (72, 0, 24, 24),
    5: (96, 0, 24, 24),
    6: (120, 0, 24, 24),
    7: (144, 0, 24, 24),
    8: (168, 0, 24, 24),
    9: (192, 0, 24, 24),
    10: (216, 0, 24, 24),
    11: (240, 0, 24, 24),
    12: (0, 24, 24, 24),
    13: (24, 24, 24, 24),
    14: (48, 24, 24, 24),
    15: (72, 24, 24, 24),
    16: (96, 24, 24, 48),
    17: (120, 24, 48, 24),
}
