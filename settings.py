"""This file contains all the settings for Pacman."""
from enum import IntEnum, Enum

# Colors
class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    CYAN = (43, 255, 255)


# Pacman settings
TOLERANCE = 3
SPEED = 4
class Directions(Enum):
    """Enum for the possible movement directions of characters."""

    NONE  = (0,  0,  0)
    UP    = (0, -1,  1)
    RIGHT = (1,  0,  2)
    DOWN  = (0,  1,  4)
    LEFT  = (-1, 0,  8)

    @property
    def dx(self): return self.value[0]
    @property
    def dy(self): return self.value[1]
    @property
    def bit(self): return self.value[2]

# Maze settings
class Tile(IntEnum):
    """Enum for the different types of tiles in the maze."""

    FLOOR = 0
    WALL = 1
    CORNER = 2

WALL_SIZE = 14
FLOOR_SIZE = 50
CELL_SIZE = WALL_SIZE + FLOOR_SIZE
HEIGHT = 15
WIDTH = 20
MAZE_SIZE = HEIGHT * WIDTH
TILEMAP_WIDTH = WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * WIDTH
TILEMAP_HEIGHT = WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * HEIGHT

# Screen settings
OFFSET_X = 60
OFFSET_Y = 60
SCREEN_SIZE = (
    TILEMAP_WIDTH + 2 * OFFSET_X,
    TILEMAP_HEIGHT + 2 * OFFSET_Y
    )
FPS = 60

# Pacgum settings
RADIUS = 3
