import math
from pygame import Rect, Surface
from settings import TOLERANCE, FLOOR_SIZE, WALL_SIZE, Directions
from .character import Character
from spritesheet import Spritesheet


class Ghost(Character):
    INITIAL_DIRECTION: Directions = Directions.NONE
    SPRITES: dict[Directions, list[tuple[int, int, int, int]]] = {}

    def __init__(
            self, maze: list[list[int]],
            pacman: Character,
            spritesheet: Spritesheet
            ):
        self.spritesheet = spritesheet
        self.animation: dict[Directions, list[Surface]] = {}
        self.pacman: Character = pacman
        self.available_dir: list[Directions] = []
        super().__init__(maze, spritesheet)

    def _distance_target(self, pos, target_pos: tuple[int, int]):
        pos_x, pos_y = pos
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
    INITIAL_DIRECTION = Directions.DOWN
    SPRITES = {
        Directions.RIGHT: [(0, 0, 42, 42), (48, 0, 42, 42)],
        Directions.LEFT: [(96, 0, 42, 42), (144, 0, 42, 42)],
        Directions.UP: [(192, 0, 42, 42), (240, 0, 42, 42)],
        Directions.DOWN: [(288, 0, 42, 42), (336, 0, 42, 42)],
    }

    def __init__(
            self,
            maze: list[list[int]],
            pacman: Character,
            spritesheet: Spritesheet
            ):
        super().__init__(maze, pacman, spritesheet)

    def update(self) -> None:
        cx, cy = self._current_cell()
        center_x, center_y = self._to_pixels(cx, cy)
        at_center = (abs(center_x - self.rect.centerx) < TOLERANCE
                     and abs(center_y - self.rect.centery) < TOLERANCE)

        if at_center:
            self.rect.center = (center_x, center_y)
            for d in Directions:
                if self._can_move(d, cx, cy):
                    print(f"Can move {d} from ({cx}, {cy})")
                    if (
                        self._direction != Directions.NONE
                        and d == self._opposite_direction(self._direction)
                    ):
                        continue
                    self.available_dir.append(d)

            if not self.available_dir:
                self._direction = self._opposite_direction(self._direction)

            min_dist = self._distance_target(
                self.rect.center,
                self.pacman._current_cell()
                )

            if self.available_dir:
                if len(self.available_dir) == 1:
                    self._direction = self.available_dir[0]
                else:
                    for d in self.available_dir:
                        nx = cx + d.dx
                        ny = cy + d.dy
                        new_dist = self._distance_target(
                            (nx, ny),
                            self.pacman._current_cell()
                            )
                        if new_dist < min_dist:
                            min_dist = new_dist
                            self._direction = d

        self.rect.x += self._direction.dx * self.speed
        self.rect.y += self._direction.dy * self.speed

        self.available_dir.clear()

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
    INITIAL_DIRECTION = Directions.UP

    def __init__(self, maze: list[list[int]], pacman: Character, spritesheet: Spritesheet):
        super().__init__(maze, pacman, spritesheet)

    def move(self, pacman_pos: tuple, pacman_dir: str):
        pass  # anticipa di 4 tile


class Inky(Ghost):
    INITIAL_DIRECTION = Directions.RIGHT

    def __init__(self, maze: list[list[int]], pacman: Character, spritesheet: Spritesheet):
        super().__init__(maze, pacman, spritesheet)

    def move(self, pacman_pos: tuple, blinky_pos: tuple):
        pass  # comportamento misto


class Clyde(Ghost):
    INITIAL_DIRECTION = Directions.DOWN

    def __init__(self, maze: list[list[int]], pacman: Character, spritesheet: Spritesheet):
        super().__init__(maze, pacman, spritesheet)

    def move(self, pacman_pos: tuple):
        pass  # random quando lontano, scappa quando vicino
