import pygame


class MazeSpritesheet:
    def __init__(self, spritesheet):
        self.spritesheet = spritesheet

    def get_sprite(self, x, y, width, height):
        sprite = self.spritesheet.subsurface(pygame.Rect(x, y, width, height))
        return sprite


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

if __name__ == "__main__":
    from pathlib import Path

    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    current_dir = Path(__file__).parent
    spritesheet_image = pygame.image.load(current_dir / "maze_tiles11.png")
    spritesheet = MazeSpritesheet(spritesheet_image)

    screen.blit(spritesheet.get_sprite(*Tiles[17]), (0, 0))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
