import math
import sys

from pygame import Rect, Surface

from settings import TOLERANCE, FLOOR_SIZE, WALL_SIZE, Directions

from .character import Character


class Ghost(Character):
    GHOST_NAME: str | None = None
    INITIAL_DIRECTION: Directions = Directions.NONE
    SCARED_DIR: str = "ghosts/scared"

    def __init__(self, maze: list[list[int]], pacman: Character):
        self.animation: dict[Directions, list[Surface]] = {}
        self.scared_anim: list[Surface] = []
        self.scared = False
        self.pacman: Character = pacman
        self.i = 0
        super().__init__(maze)

    def _load_image(self) -> tuple[Surface, Rect]:
        if self.GHOST_NAME:
            self.animation = {
                Directions.UP: self._load_anim(
                    f"{self.GHOST_NAME}/{self.GHOST_NAME.split('/')[-1]}-up"
                ),
                Directions.LEFT: self._load_anim(
                    f"{self.GHOST_NAME}/{self.GHOST_NAME.split('/')[-1]}-left"
                ),
                Directions.DOWN: self._load_anim(
                    f"{self.GHOST_NAME}/{self.GHOST_NAME.split('/')[-1]}-down"
                ),
                Directions.RIGHT: self._load_anim(
                    f"{self.GHOST_NAME}/{self.GHOST_NAME.split('/')[-1]}-right"
                ),
            }
        self.scared_anim = self._load_anim(self.SCARED_DIR)

        image = self.animation[self.INITIAL_DIRECTION][0]
        return image, image.get_rect()

    def _distance_target(self, target_pos: tuple[int, int]):
        pos_x, pos_y = self.rect.center
        target_x, target_y = target_pos

        return math.sqrt((target_x - pos_x) ** 2 + (target_y - pos_y) ** 2)

    def _opposite_direction(self, direction: Directions) -> Directions:
        if direction == Directions.UP:
            return Directions.DOWN
        elif direction == Directions.DOWN:
            return Directions.UP
        elif direction == Directions.LEFT:
            return Directions.RIGHT
        elif direction == Directions.RIGHT:
            return Directions.LEFT
        else:
            return Directions.NONE

    def respawn(self) -> None:
        raise NotImplementedError("Each ghost must define its own respawn")


class Blinky(Ghost):
    GHOST_NAME = "ghosts/blinky"
    INITIAL_DIRECTION = Directions.DOWN

    def __init__(self, maze: list[list[int]], pacman: Character):
        super().__init__(maze, pacman)

    def update(self) -> None:
        available_dir = []
        print(f"Available directions: {available_dir}")
        cx, cy = self._current_cell()
        center_x, center_y = self._to_pixels(cx, cy)
        print(f"Current cell: ({cx}, {cy}), center: ({center_x}, {center_y}), rect center: {self.rect.center})")
        at_center = (abs(center_x - self.rect.centerx) < TOLERANCE
                     and abs(center_y - self.rect.centery) < TOLERANCE)
        print(f"At center: {at_center}")

        if at_center:
            self.rect.center = (center_x, center_y)
            for d in Directions:
                if self._can_move(d, cx, cy):
                    if (
                        self._direction != Directions.NONE
                        and d == self._opposite_direction(self._direction)
                    ):
                        continue
                    available_dir.append(d)

        if not available_dir:
            self._direction = self._opposite_direction(self._direction)

        min_dist = self._distance_target(self.pacman.rect.center)

        print(available_dir)
        if available_dir:
            if len(available_dir) == 1:
                self._direction = available_dir[0]
            else:
                for d in available_dir:
                    nx, ny = self._to_pixels(cx + d.dx, cy + d.dy)
                    new_dist = self._distance_target((nx, ny))
                    if new_dist < min_dist:
                        min_dist = new_dist
                        self._direction = d

        print(self._direction)
        if self._direction in (Directions.LEFT, Directions.RIGHT):
            self.rect.x += self._direction.dx * self.speed
        elif self._direction in (Directions.UP, Directions.DOWN):
            self.rect.y += self._direction.dy * self.speed

        if self._direction != Directions.NONE:
            current_center = self.rect.center
            frame = self.animation[self._direction]
            self.frame_slower += 0.2
            if self.frame_slower >= len(frame):
                self.frame_slower = 0
            self.image = frame[int(self.frame_slower)]
            self.rect = self.image.get_rect(center=current_center)
        self.i += 1
        if self.i == 3:
            sys.exit("Blinky is the only ghost implemented for now, other ghosts will be implemented in the next iterations")

    def respawn(self) -> None:
        pos_x = WALL_SIZE + FLOOR_SIZE // 2
        pos_y = WALL_SIZE + FLOOR_SIZE // 2

        self.rect.center = (pos_x, pos_y)


class Pinky(Ghost):
    GHOST_NAME = "ghosts/pinky"
    INITIAL_DIRECTION = Directions.UP

    def __init__(self, maze: list[list[int]], pacman: Character):
        super().__init__(maze, pacman)

    def move(self, pacman_pos: tuple, pacman_dir: str):
        pass  # anticipa di 4 tile


class Inky(Ghost):
    GHOST_NAME = "ghosts/inky"
    INITIAL_DIRECTION = Directions.RIGHT

    def __init__(self, maze: list[list[int]], pacman: Character):
        super().__init__(maze, pacman)

    def move(self, pacman_pos: tuple, blinky_pos: tuple):
        pass  # comportamento misto


class Clyde(Ghost):
    GHOST_NAME = "ghosts/clyde"
    INITIAL_DIRECTION = Directions.DOWN

    def __init__(self, maze: list[list[int]], pacman: Character):
        super().__init__(maze, pacman)

    def move(self, pacman_pos: tuple):
        pass  # random quando lontano, scappa quando vicino
