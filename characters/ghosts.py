import math
from abc import abstractmethod, ABC
from pygame import Surface
from settings import TOLERANCE, FLOOR_SIZE, WALL_SIZE, CELL_SIZE, Directions
from .pacman import Pacman
from .character import Character
from spritesheet import Spritesheet


class Ghost(Character, ABC):
    INITIAL_DIRECTION: Directions = Directions.NONE
    SPRITES: dict[Directions, list[tuple[int, int, int, int]]] = {}

    def __init__(
            self, maze: list[list[int]],
            pacman: Pacman,
            spritesheet: Spritesheet
            ):
        if maze is None or spritesheet is None:
            raise TypeError("The Ghost requires maze and spritesheet")
        self.spritesheet = spritesheet
        self.animation: dict[Directions, list[Surface]] = {}
        self.pacman: Pacman = pacman
        self.available_dir: list[Directions] = []
        self.speed = 0.85 * self.pacman.speed
        super().__init__(maze, spritesheet)

    def _distance_target(self, pos, target_pos: tuple[int, int]):
        pos_x, pos_y = pos
        target_x, target_y = target_pos

        return math.sqrt((target_x - pos_x) ** 2 + (target_y - pos_y) ** 2)

    @abstractmethod
    def _target_cell(self) -> tuple[int, int]:
        ...

    def _chase(self) -> None:
        cx, cy = self._current_cell()
        center_x, center_y = self._to_pixels(cx, cy)
        at_center = (abs(center_x - self.rect.centerx) < TOLERANCE
                     and abs(center_y - self.rect.centery) < TOLERANCE)

        if at_center:
            for d in Directions:
                if self._can_move(d, cx, cy):
                    if (
                        self._direction != Directions.NONE
                        and d == self._opposite_direction(self._direction)
                    ):
                        continue
                    self.available_dir.append(d)

            if not self.available_dir:
                self._direction = self._opposite_direction(self._direction)

            target_cell = self._target_cell()
            min_dist = self._distance_target(
                self.rect.center,
                target_cell
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
                            target_cell
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

    def _scatter(self) -> None:
        pass

    def update(self) -> None:
        self._chase()

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
            pacman: Pacman,
            spritesheet: Spritesheet
            ):
        super().__init__(maze, pacman, spritesheet)

    def _target_cell(self) -> tuple[int, int]:
        return self.pacman._current_cell()

    def respawn(self) -> None:
        pos_x = WALL_SIZE + FLOOR_SIZE // 2
        pos_y = WALL_SIZE + FLOOR_SIZE // 2

        self.rect.center = (pos_x, pos_y)


class Pinky(Ghost):
    INITIAL_DIRECTION = Directions.DOWN
    SPRITES = {
        Directions.RIGHT: [(0, 48, 42, 42), (48, 48, 42, 42)],
        Directions.LEFT: [(96, 48, 42, 42), (144, 48, 42, 42)],
        Directions.UP: [(192, 48, 42, 42), (240, 48, 42, 42)],
        Directions.DOWN: [(288, 48, 42, 42), (336, 48, 42, 42)],
    }

    def __init__(
            self,
            maze: list[list[int]],
            pacman: Pacman,
            spritesheet: Spritesheet
            ):
        super().__init__(maze, pacman, spritesheet)

    def _target_cell(self) -> tuple[int, int]:
        px, py = self.pacman._current_cell()
        return (
            px + self.pacman.direction.dx * 4,
            py + self.pacman.direction.dy * 4,
        )

    def respawn(self) -> None:
        pos_x = (
            CELL_SIZE * (len(self.maze[0]) - 1)
            + WALL_SIZE
            + FLOOR_SIZE // 2
        )
        pos_y = WALL_SIZE + FLOOR_SIZE // 2

        self.rect.center = (pos_x, pos_y)


class Inky(Ghost):
    INITIAL_DIRECTION = Directions.UP
    SPRITES = {
        Directions.RIGHT: [(0, 96, 42, 42), (48, 96, 42, 42)],
        Directions.LEFT: [(96, 96, 42, 42), (144, 96, 42, 42)],
        Directions.UP: [(192, 96, 42, 42), (240, 96, 42, 42)],
        Directions.DOWN: [(288, 96, 42, 42), (336, 96, 42, 42)],
    }

    def __init__(
            self,
            maze: list[list[int]],
            pacman: Pacman,
            blinky: Blinky,
            spritesheet: Spritesheet
            ):
        self.blinky = blinky
        super().__init__(maze, pacman, spritesheet)

    def _target_cell(self) -> tuple[int, int]:
        px, py = self.pacman._current_cell()
        bx, by = self.blinky._current_cell()

        pivot_x = px + self.pacman.direction.dx * 2
        pivot_y = py + self.pacman.direction.dy * 2

        return (
            pivot_x + (pivot_x - bx),
            pivot_y + (pivot_y - by)
        )

    def respawn(self) -> None:
        pos_x = WALL_SIZE + FLOOR_SIZE // 2
        pos_y = CELL_SIZE * (len(self.maze) - 1) + WALL_SIZE + FLOOR_SIZE // 2

        self.rect.center = (pos_x, pos_y)


class Clyde(Ghost):
    INITIAL_DIRECTION = Directions.UP
    SPRITES = {
        Directions.RIGHT: [(0, 144, 42, 42), (48, 144, 42, 42)],
        Directions.LEFT: [(96, 144, 42, 42), (144, 144, 42, 42)],
        Directions.UP: [(192, 144, 42, 42), (240, 144, 42, 42)],
        Directions.DOWN: [(288, 144, 42, 42), (336, 144, 42, 42)],
    }

    def __init__(
            self,
            maze: list[list[int]],
            pacman: Pacman,
            spritesheet: Spritesheet
            ):
        super().__init__(maze, pacman, spritesheet)

    def _target_cell(self) -> tuple[int, int]:
        cx, cy = self._current_cell()
        px, py = self.pacman._current_cell()
        distance = self._distance_target((cx, cy), (px, py))

        if distance > 8:
            return (px, py)
        else:
            return (len(self.maze[0]) - 1, len(self.maze) - 1)

    def respawn(self) -> None:
        pos_x = (
            CELL_SIZE * (len(self.maze[0]) - 1)
            + WALL_SIZE
            + FLOOR_SIZE // 2
        )
        pos_y = CELL_SIZE * (len(self.maze) - 1) + WALL_SIZE + FLOOR_SIZE // 2

        self.rect.center = (pos_x, pos_y)
