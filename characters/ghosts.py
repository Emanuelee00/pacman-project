import math

from pygame import Rect, Surface

from settings import TOLERANCE, FLOOR_SIZE, WALL_SIZE, Directions

from .character import Character


class Ghost(Character):
    GHOST_NAME: str | None = None
    INITIAL_DIRECTION: Directions | None = None
    SCARED_DIR: str = "ghosts/scared"

    def __init__(self, maze: list[list[int]], pacman: Character):
        self.animation: dict[Directions, list[Surface]] = {}
        self.scared_anim: list[Surface] = []
        self.scared = False
        self.pacman: Character = pacman
        super().__init__(maze)

    def _load_image(self) -> tuple[Surface, Rect]:
        if self.GHOST_NAME:
            self.animation = {
                Directions.UP: self._load_anim(
                    f"{self.GHOST_NAME}/{self.GHOST_NAME}-up"
                ),
                Directions.LEFT: self._load_anim(
                    f"{self.GHOST_NAME}/{self.GHOST_NAME}-left"
                ),
                Directions.DOWN: self._load_anim(
                    f"{self.GHOST_NAME}/{self.GHOST_NAME}-down"
                ),
                Directions.RIGHT: self._load_anim(
                    f"{self.GHOST_NAME}/{self.GHOST_NAME}-right"
                ),
            }
        self.scared_anim = self._load_anim(self.SCARED_DIR)

        if self.INITIAL_DIRECTION:
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
    DIRECTION_DIR = "ghosts/blinky"
    INITIAL_DIRECTION = Directions.LEFT

    def __init__(self, maze: list[list[int]], pacman: Character):
        super().__init__(maze, pacman)

    def update(self) -> None:
        available_dir = []
        cx, cy = self._current_cell()
        center_x, center_y = self._to_pixels(cx, cy)
        at_center = (abs(center_x - self.rect.centerx) < TOLERANCE
                     and abs(center_y - self.rect.centery))

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

        if self._direction in (Directions.LEFT, Directions.RIGHT):
            self.rect.centerx += self._direction.dx * self.speed
        elif self._direction in (Directions.UP, Directions.DOWN):
            self.rect.centery += self._direction.dy * self.speed

        if self._direction != Directions.NONE:
            current_center = self.rect.center
            frame = self.animation[self._direction]
            self.frame_slower += 0.2
            if self.frame_slower >= len(frame):
                self.frame_slower = 0
            self.image = frame[int(self.frame_slower)]
            self.rect = self.image.get_rect(center=current_center)

    def respawn(self) -> None:
        pos_x = WALL_SIZE + FLOOR_SIZE // 2
        pos_y = WALL_SIZE + FLOOR_SIZE // 2

        self.rect.center = (pos_x, pos_y)


class Pinky(Ghost):
    DIRECTION_DIR = "ghosts/pinky"
    INITIAL_DIRECTION = Directions.UP

    def __init__(self, maze: list[list[int]], pacman: Character):
        super().__init__(maze, pacman)

    def move(self, pacman_pos: tuple, pacman_dir: str):
        pass  # anticipa di 4 tile


class Inky(Ghost):
    DIRECTION_DIR = "ghosts/inky"
    INITIAL_DIRECTION = Directions.RIGHT

    def __init__(self, maze: list[list[int]], pacman: Character):
        super().__init__(maze, pacman)

    def move(self, pacman_pos: tuple, blinky_pos: tuple):
        pass  # comportamento misto


class Clyde(Ghost):
    DIRECTION_DIR = "ghosts/clyde"
    INITIAL_DIRECTION = Directions.DOWN

    def __init__(self, maze: list[list[int]], pacman: Character):
        super().__init__(maze, pacman)

    def move(self, pacman_pos: tuple):
        pass  # random quando lontano, scappa quando vicino
