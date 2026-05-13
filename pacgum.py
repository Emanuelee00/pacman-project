import pygame
from settings import CELL_SIZE, WALL_SIZE, FLOOR_SIZE, RADIUS, Color

class Pacgum(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, radius=RADIUS, is_super=False) -> None:
        super().__init__()
        self.radius = radius
        self.is_super = is_super
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(self.image, Color.YELLOW, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)


class PacgumManager:
    def __init__(self, maze) -> None:
        self.group = pygame.sprite.Group()
        self._fill_maze(maze)

    def _fill_maze(self, maze):
        def is_corner(maze, cx, cy):
            return (
                (cx == 0 and cy == 0)
                or (cx == 0 and cy == len(maze) - 1)
                or (cx == len(maze[0]) - 1 and cy == 0)
                or (cx == len(maze[0]) - 1 and cy == len(maze) - 1)
            )

        for cy in range(len(maze)):
            for cx in range(len(maze[cy])):
                if maze[cy][cx] != 15:
                    pos_x = cx * CELL_SIZE + WALL_SIZE + FLOOR_SIZE // 2
                    pos_y = cy * CELL_SIZE + WALL_SIZE + FLOOR_SIZE // 2
                    self.group.add(Pacgum(pos_x, pos_y)) if not is_corner(maze, cx, cy) else self.group.add(Pacgum(pos_x, pos_y, radius=RADIUS + 4, is_super=True))
