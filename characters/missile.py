import pygame
from pathlib import Path
from .character import Character
from spritesheet import Spritesheet
from settings import Directions, CELL_SIZE, SPEED

_FRAME_W = 718 // 7
_FRAME_H = 144
_SIZE = (24, 24)
_ROTATIONS = {
    Directions.UP: 0,
    Directions.LEFT: 90,
    Directions.DOWN: 180,
    Directions.RIGHT: 270,
}


class Missile(Character):
    SPRITES = {}
    INITIAL_DIRECTION = Directions.UP

    def __init__(self, center: tuple[int, int], direction: Directions, maze: list[list[int]]):
        self._fire_direction = direction
        spritesheet = Spritesheet(Path(__file__).parent.parent / "assets" / "missile.png")
        super().__init__(maze, spritesheet)
        self._direction = direction
        self._distance = 0
        self.rect.center = center

    def _load_image(self):
        for direction, angle in _ROTATIONS.items():
            frames = []
            for i in range(7):
                frame = self.spritesheet.get_sprite(i * _FRAME_W, 0, _FRAME_W, _FRAME_H)
                frame = pygame.transform.scale(frame, _SIZE)
                frame = pygame.transform.rotate(frame, angle)
                frames.append(frame)
            self.animation[direction] = frames
        image = self.animation[self.INITIAL_DIRECTION][0]
        return image, image.get_rect()

    def respawn(self) -> None:
        pass

    def update(self) -> None:
        cx, cy = self._current_cell()
        if not self._can_move(self._direction, cx, cy) or self._distance >= 2 * CELL_SIZE:
            self.kill()
            return

        self.rect.x += self._direction.dx * SPEED
        self.rect.y += self._direction.dy * SPEED
        self._distance += SPEED

        current_center = self.rect.center
        self.frame_slower = (self.frame_slower + 0.2) % len(self.animation[self._direction])
        self.image = self.animation[self._direction][int(self.frame_slower)]
        self.rect = self.image.get_rect(center=current_center)
