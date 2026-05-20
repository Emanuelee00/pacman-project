import pygame
import random
from pathlib import Path
from .character import Character
from spritesheet import Spritesheet
from settings import Directions, SPEED, TOLERANCE

_FRAME_W = 1536 // 7
_FRAME_H = 1024
_TARGET_H = 100
_SIZE = (max(16, _TARGET_H * _FRAME_W // _FRAME_H), _TARGET_H)
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
        self._spawn_time = pygame.time.get_ticks()
        self.rect.center = center

    def _load_image(self):
        for direction, angle in _ROTATIONS.items():
            frames = []
            for i in range(7):
                frame = self.spritesheet.get_sprite(i * _FRAME_W, 0, _FRAME_W, _FRAME_H)
                frame = pygame.transform.scale(frame, _SIZE)
                frame = pygame.transform.rotate(frame, angle)
                frame.set_colorkey((255, 255, 255))
                frames.append(frame)
            self.animation[direction] = frames
        image = self.animation[self.INITIAL_DIRECTION][0]
        return image, image.get_rect()

    def respawn(self) -> None:
        pass

    def update(self) -> None:
        if pygame.time.get_ticks() - self._spawn_time > 15000:
            self.kill()
            return

        cx, cy = self._current_cell()
        center_x, center_y = self._to_pixels(cx, cy)
        at_center = (abs(center_x - self.rect.centerx) < TOLERANCE
                     and abs(center_y - self.rect.centery) < TOLERANCE)

        if at_center:
            self.rect.center = (center_x, center_y)
            opposite = self._opposite_direction(self._direction)
            available = [
                d for d in (Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT)
                if d != opposite and self._can_move(d, cx, cy)
            ]
            prev_direction = self._direction
            if not available:
                self._direction = opposite
            else:
                self._direction = random.choice(available)
            if self._direction != prev_direction:
                self.frame_slower = 0

        self.rect.x += self._direction.dx * SPEED
        self.rect.y += self._direction.dy * SPEED

        current_center = self.rect.center
        frames = self.animation[self._direction]
        self.frame_slower = (self.frame_slower + 0.12) % len(frames)
        self.image = frames[int(self.frame_slower)]
        self.rect = self.image.get_rect(center=current_center)
