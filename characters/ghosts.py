from .character import Character
from settings import WALL_SIZE, FLOOR_SIZE, CELL_SIZE
import math
import random


class Ghost(Character):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.animation = self.load_anim(f"ghosts/{self.name}")
        if not self.animation:
            raise ValueError(f"Ghost '{name}' not found — check the folder name")
        self.scared_anim = self.load_anim("ghosts/scared")
        self.scared = False
        self.frame_slower = 0
        self.image = self.animation[0]
        self.rect = self.image.get_rect()

    @property
    def center(self):
        return self.rect.center

    def _distance_target(self, target_pos: tuple):
        pos_x, pos_y = self.center
        target_x, target_y = target_pos

        return math.sqrt((target_x - pos_x) ** 2 + (target_y - pos_y) ** 2)

    def _current_cell(self, maze):
        center_x, center_y = self.center
        cx = max(0, min((center_x - WALL_SIZE) // CELL_SIZE, len(maze[0]) - 1))
        cy = max(0, min((center_y - WALL_SIZE) // CELL_SIZE, len(maze) - 1))
        return cx, cy

    def update(self, maze):
        print(self._current_cell(maze))
        if self.scared:
            anim = self.scared_anim
            self.frame_slower += 0.05
        else:
            anim = self.animation
        self.frame_slower += 0.05
        if self.frame_slower >= len(anim):
            self.frame_slower = 0
        self.image = anim[int(self.frame_slower)]

    def respawn(self):
        return super().respawn()


class Blinky(Ghost):
    def __init__(self):
        super().__init__("blinky")

    def respawn(self, maze):
        pos_x = WALL_SIZE + FLOOR_SIZE // 2
        pos_y = WALL_SIZE + FLOOR_SIZE // 2

        self.rect.center = (pos_x, pos_y)

class Pinky(Ghost):
    def __init__(self):
        super().__init__("pinky")

    def move(self, pacman_pos: tuple, pacman_dir: str):
        pass  # anticipa di 4 tile


class Inky(Ghost):
    def __init__(self):
        super().__init__("inky")

    def move(self, pacman_pos: tuple, blinky_pos: tuple):
        pass  # comportamento misto


class Clyde(Ghost):
    def __init__(self):
        super().__init__("clyde")

    def move(self, pacman_pos: tuple):
        pass  # random quando lontano, scappa quando vicino
