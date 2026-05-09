import pygame
from .character import Character
from settings import Directions, CELL_SIZE, WALL_SIZE, FLOOR_SIZE, TOLERANCE, SPEED


class Pacman(Character):
    def __init__(self, *groups: pygame.sprite.AbstractGroup):
        super().__init__()
        self._direction: Directions = Directions.NONE
        self._next_direction: Directions = Directions.NONE

        self.frame_slower = 0
        self.animation = {
            Directions.UP: self.load_anim("pacman/pacman-up"),
            Directions.LEFT: self.load_anim("pacman/pacman-left"),
            Directions.RIGHT: self.load_anim("pacman/pacman-right"),
            Directions.DOWN: self.load_anim("pacman/pacman-down"),
        }
        self.image = self.animation[Directions.RIGHT][0]
        self.radius = self.image.get_width() // 2

        self.rect = self.image.get_rect()
        self.rect.center = (18 + self.radius, 18 + self.radius)

    @property
    def center(self):
        return self.rect.center

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

    def _current_cell(self, maze):
        center_x, center_y = self.center
        cx = max(0, min((center_x - WALL_SIZE) // CELL_SIZE, len(maze[0]) - 1))
        cy = max(0, min((center_y - WALL_SIZE) // CELL_SIZE, len(maze) - 1))
        return cx, cy

    def _snap_to_cell(self, cx, cy):
        snap_x = cx * CELL_SIZE + WALL_SIZE + FLOOR_SIZE // 2
        snap_y = cy * CELL_SIZE + WALL_SIZE + FLOOR_SIZE // 2
        return snap_x, snap_y

    @staticmethod
    def _can_move(direction, dx, dy, maze):
        if direction == Directions.NONE: return False
        if not (0 <= dy < len(maze) and 0 <= dx < len(maze[dy])): return False
        return not (maze[dy][dx] & direction.bit)

    def update(self, maze):
        cx, cy = self._current_cell(maze)
        snap_x, snap_y = self._snap_to_cell(cx, cy)
        center_x, center_y = self.center
        at_center = (abs(center_x - snap_x) < TOLERANCE
                and abs(center_y - snap_y) < TOLERANCE)
        if at_center:
            self.rect.center = (snap_x, snap_y)
            if self._can_move(self._next_direction, cx, cy, maze):
                self._direction = self._next_direction
            elif not self._can_move(self._direction, cx, cy, maze):
                self._direction = Directions.NONE

        if self._direction in (Directions.LEFT, Directions.RIGHT):
            self.rect.centery = snap_y
            self.rect.x += self._direction.dx * SPEED
        elif self._direction in (Directions.UP, Directions.DOWN):
            self.rect.centerx = snap_x
            self.rect.y += self._direction.dy * SPEED

        if self._direction != Directions.NONE:
            current_center = self.rect.center
            frame = self.animation[self._direction]
            self.frame_slower += 0.2
            if self.frame_slower >= len(frame):
                self.frame_slower = 0
            self.image = frame[int(self.frame_slower)]
            self.rect = self.image.get_rect(center=current_center)

    def respawn(self, maze):
        center_maze_y = len(maze) // 2
        center_maze_x = len(maze[0]) // 2

        pos_x = center_maze_x * CELL_SIZE + WALL_SIZE + FLOOR_SIZE // 2
        pos_y = center_maze_y * CELL_SIZE + WALL_SIZE + FLOOR_SIZE // 2

        if maze[center_maze_y][center_maze_x] != 15:
            self.rect.center = (pos_x, pos_y)
        else:
            directions = [Directions.LEFT, Directions.RIGHT]
            for direction in directions:
                if maze[center_maze_y + direction.dy][center_maze_x + direction.dx] != 15:
                    pos_x = (center_maze_x + direction.dx) * CELL_SIZE + WALL_SIZE + FLOOR_SIZE // 2
                    pos_y = (center_maze_y + direction.dy)* CELL_SIZE + WALL_SIZE + FLOOR_SIZE // 2
                    self.rect.center = (pos_x + direction.dx, pos_y + direction.dy)
