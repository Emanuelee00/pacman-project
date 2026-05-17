import pygame
from pygame import Surface, Rect
from settings import (
    Directions,
    SPEED,
    WALL_SIZE,
    FLOOR_SIZE,
    CELL_SIZE,
)
from abc import ABC, abstractmethod
from spritesheet import Spritesheet


class Character(pygame.sprite.Sprite, ABC):
    SIZE = (40, 40)
    SPRITES = {}
    INITIAL_DIRECTION = Directions.NONE

    def __init__(self, maze: list[list[int]], spritesheet: Spritesheet):
        super().__init__()
        self.maze: list[list[int]] = maze
        self.spritesheet = spritesheet
        self._direction: Directions = Directions.NONE
        self.animation = {}
        self.image, self.rect = self._load_image()
        self.speed = SPEED
        self.frame_slower = 0

    def _load_image(self) -> tuple[Surface, Rect]:
        for direction, coords in self.SPRITES.items():
            self.animation[direction] = [
                self.spritesheet.get_sprite(*rect) for rect in coords
            ]
        image = self.animation[self.INITIAL_DIRECTION][0]
        return image, image.get_rect()

    @abstractmethod
    def respawn(self) -> None:
        pass

    def _current_cell(self) -> tuple[int, int]:
        cx = max(
            0,
            min(
                (self.rect.centerx - WALL_SIZE) // CELL_SIZE,
                len(self.maze[0]) - 1,
            ),
        )
        cy = max(
            0,
            min(
                (self.rect.centery - WALL_SIZE) // CELL_SIZE,
                len(self.maze) - 1,
            ),
        )
        return cx, cy

    def _to_pixels(self, cx, cy) -> tuple[int, int]:
        center_x = cx * CELL_SIZE + WALL_SIZE + FLOOR_SIZE // 2
        center_y = cy * CELL_SIZE + WALL_SIZE + FLOOR_SIZE // 2
        return center_x, center_y

    def _can_move(self, direction, dx, dy) -> bool:
        if direction == Directions.NONE:
            return False
        if not (0 <= dy < len(self.maze) and 0 <= dx < len(self.maze[dy])):
            return False
        return not (self.maze[dy][dx] & direction.bit)

    @abstractmethod
    def update(self) -> None:
        pass
