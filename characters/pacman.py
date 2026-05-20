import pygame
from pathlib import Path

from spritesheet import Spritesheet
from .character import Character
from settings import (
    Directions,
    SPEED,
)
from pygame import Surface


class Pacman(Character):
    INITIAL_DIRECTION = Directions.RIGHT
    SPRITES = {
        Directions.RIGHT: [
            (0, 54, 48, 48),
            (54, 54, 48, 48),
            (108, 54, 48, 48),
        ],
        Directions.LEFT: [
            (162, 54, 48, 48),
            (216, 54, 48, 48),
            (270, 54, 48, 48),
        ],
        Directions.UP: [(0, 0, 48, 48), (54, 0, 48, 48), (108, 0, 48, 48)],
        Directions.DOWN: [
            (162, 0, 48, 48),
            (216, 0, 48, 48),
            (270, 0, 48, 48),
        ],
        "dead": [
            (0, 128, 48, 48),
            (54, 128, 48, 48),
            (108, 128, 48, 48),
            (162, 128, 48, 48),
            (216, 128, 48, 48),
            (270, 128, 48, 48)],
    }

    def __init__(
            self,
            *groups: pygame.sprite.AbstractGroup,
            maze: list[list[int]] | None = None,
            spritesheet: Spritesheet | None = None,
            ) -> None:
        if maze is None or spritesheet is None:
            raise TypeError("Pacman requires maze and spritesheet")
        self.animation: dict[Directions, list[Surface]] = {}
        self.spritesheet = spritesheet
        super().__init__(maze, spritesheet, *groups)

        self._next_direction: Directions = Directions.NONE
        self._frame_slower = 0
        self.speed = SPEED
        self._cheated = False
        self.is_alive = True

    @property
    def direction(self):
        return self._direction

    @property
    def next_direction(self):
        return self._next_direction

    @next_direction.setter
    def next_direction(self, keys):
        if keys[pygame.K_LEFT]:
            self._next_direction = Directions.LEFT
        elif keys[pygame.K_RIGHT]:
            self._next_direction = Directions.RIGHT
        elif keys[pygame.K_UP]:
            self._next_direction = Directions.UP
        elif keys[pygame.K_DOWN]:
            self._next_direction = Directions.DOWN

    def update(self) -> None:
        cx, cy = self._current_cell()
        center_x, center_y = self._to_pixels(cx, cy)
        at_center = (abs(center_x - self.rect.centerx) < self.speed
                     and abs(center_y - self.rect.centery) < self.speed)

        if (at_center or
           self._next_direction == self._opposite_direction(self._direction)):
            if at_center:
                self.rect.center = (center_x, center_y)
            if self._can_move(self._next_direction, cx, cy):
                self._direction = self._next_direction
            elif not self._can_move(self._direction, cx, cy):
                self._direction = Directions.NONE

        self.rect.x += self._direction.dx * self.speed
        self.rect.y += self._direction.dy * self.speed

        if self.is_alive and self._direction != Directions.NONE:
            current_center = self.rect.center
            frame = self.animation[self._direction]
            self.frame_slower += 0.2
            if self.frame_slower >= len(frame):
                self.frame_slower = 0
            self.image = frame[int(self.frame_slower)]
            self.rect = self.image.get_rect(center=current_center)
        # else:
        #     self.image = self.animation["dead"][0]

    def respawn(self) -> None:
        # Center of the maze
        cmy = len(self.maze) // 2
        cmx = len(self.maze[0]) // 2

        pos_x, pos_y = self._to_pixels(cmx, cmy)

        if self.maze[cmy][cmx] != 15:
            self.rect.center = (pos_x, pos_y)
        else:
            directions = [Directions.LEFT, Directions.RIGHT]
            for direc in directions:
                if self.maze[cmy + direc.dy][cmx + direc.dx] != 15:
                    pos_x, pos_y = self._to_pixels(
                        cmx + direc.dx, cmy + direc.dy
                        )
                    self.rect.center = (pos_x + direc.dx, pos_y + direc.dy)

    def shoot(self, missiles_group) -> None:
        from .missile import Missile
        if not self._cheated:
            return
        for direction in (Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT):
            missiles_group.add(Missile(self.rect.center, direction, self.maze))

    def set_normal(self):
        self._cheated = False
        self.SIZE = Character.SIZE
        self.speed = SPEED
        self.animation = {
            Directions.UP: self._load_anim("pacman/pacman-up"),
            Directions.LEFT: self._load_anim("pacman/pacman-left"),
            Directions.RIGHT: self._load_anim("pacman/pacman-right"),
            Directions.DOWN: self._load_anim("pacman/pacman-down"),
        }
        self.image = self.animation[Directions.RIGHT][0]
        self.rect = self.image.get_rect(center=self.rect.center)


    def _load_anim(self, folder: str):
        base = Path(__file__).parent.parent
        assets = Path(base / "assets" / folder)

        self.walk_anim = []
        for file in assets.iterdir():
            img = pygame.image.load(Path(assets / file))
            img = pygame.transform.scale(img, self.SIZE)
            self.walk_anim.append(img)

        return self.walk_anim

    def set_cheated(self):
        self._cheated = True
        self.SIZE = (100, 100)
        self.speed = 23
        self.animation = {
            Directions.UP: self._load_anim("pacman_car/pacman-up"),
            Directions.LEFT: self._load_anim("pacman_car/pacman-left"),
            Directions.RIGHT: self._load_anim("pacman_car/pacman-right"),
            Directions.DOWN: self._load_anim("pacman_car/pacman-down"),
        }
        self.image = self.animation[Directions.RIGHT][0]
        self.rect = self.image.get_rect(center=self.rect.center)
