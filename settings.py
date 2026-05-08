"""This file contains all the settings for Pacman."""
from enum import IntEnum, Enum



# Pacman settings
TOLERANCE = 3
SPEED = 3
class Directions(tuple, Enum):
    """Enum for the 4 directions"""

    NONE = (0, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def dx(self):
        return self.value[0]

    @property
    def dy(self):
        return self.value[1]

# Maze settings
class Tile(IntEnum):
    """Enum for the different types of tiles in the maze."""

    FLOOR = 0
    WALL = 1
    CORNER = 2

WALL_SIZE = 12
FLOOR_SIZE = 50
HEIGHT = 15
WIDTH = 15
MAZE_SIZE = HEIGHT * WIDTH
OFFSET_X = 60
OFFSET_Y = 60
COLOR = (0, 0, 255)

# Screen settings
SCREEN_SIZE = (
    WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * WIDTH,
    WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * HEIGHT
    )
