import pygame
import pygame.gfxdraw
from settings import Tile, HEIGHT, WIDTH, FLOOR_SIZE, WALL_SIZE, Color
from mazegenerator.mazegenerator import MazeGenerator
from characters.pacman import Pacman

WS = WALL_SIZE

def _draw_arc_twice(screen, cx, cy, radius, start_angle, end_angle, color):
    for dr in range(2):
        pygame.gfxdraw.arc(screen, cx, cy, radius - dr, start_angle, end_angle, color)

CORNER_DRAWER = {
    1: lambda surface, x_start, y_start: _draw_arc_twice(
        surface, x_start + WS // 2, y_start, (WS // 2) - 1, 0, 180, Color.BLUE
        ),
    2: lambda surface, x_start, y_start: _draw_arc_twice(
        surface, x_start + WS, y_start + WS // 2, (WS // 2) - 1, 90, 270, Color.BLUE
        ),
    3: lambda surface, x_start, y_start: _draw_arc_twice(
        surface, x_start + WS, y_start, WS, 90, 180, Color.BLUE
        ),
    4: lambda surface, x_start, y_start: _draw_arc_twice(
        surface, x_start + WS // 2, y_start + WS, (WS // 2) - 1, 180, 360, Color.BLUE
        ),
    5: lambda surface, x_start, y_start: (
        pygame.draw.line(surface, Color.BLUE, (x_start, y_start), (x_start, y_start + WS), width=2),
        pygame.draw.line(surface, Color.BLUE, (x_start + WS, y_start), (x_start + WS, y_start + WS), width=2)
        ),
    6: lambda surface, x_start, y_start: _draw_arc_twice(
        surface, x_start + WS, y_start + WS, WS, 180, 270, Color.BLUE
        ),
    7: lambda surface, x_start, y_start: pygame.draw.line(
        surface, Color.BLUE, (x_start, y_start), (x_start, y_start + WS), width=2
        ),
    8: lambda surface, x_start, y_start: _draw_arc_twice(
        surface, x_start, y_start + WS // 2, (WS // 2) - 1, 270, 450, Color.BLUE
        ),
    9: lambda surface, x_start, y_start: _draw_arc_twice(
        surface, x_start, y_start, WS, 0, 90, Color.BLUE
        ),
    10: lambda surface, x_start, y_start: (
        pygame.draw.line(surface, Color.BLUE, (x_start, y_start), (x_start + WS, y_start), width=2),
        pygame.draw.line(surface, Color.BLUE, (x_start, y_start + WS), (x_start + WS, y_start + WS), width=2)
        ),
    11: lambda surface, x_start, y_start: pygame.draw.line(
        surface, Color.BLUE, (x_start, y_start + WS), (x_start + WS, y_start + WS), width=2
        ),
    12: lambda surface, x_start, y_start: _draw_arc_twice(
        surface, x_start, y_start + WS, WS, 270, 360, Color.BLUE
        ),
    13: lambda surface, x_start, y_start: pygame.draw.line(
        surface, Color.BLUE, (x_start + WS, y_start), (x_start + WS, y_start + WS), width=2
        ),
    14: lambda surface, x_start, y_start: pygame.draw.line(
        surface, Color.BLUE, (x_start, y_start), (x_start + WS, y_start), width=2
        ),
}


def to_tile_map(maze) -> list:
    tile_map = []

    for ty in range(2 * len(maze) + 1):
        row = []
        for tx in range(2 * len(maze[0]) + 1):
            x = tx // 2
            y = ty // 2

            if tx % 2 == 1 and ty % 2 == 1:
                row.append(Tile.FLOOR)

            elif tx % 2 == 1 and ty % 2 == 0:
                if ty == 0 or ty == 2 * len(maze):
                    row.append(Tile.WALL)
                # Internal horizontal wall: check SOUTH wall of cell above.
                elif 0 < y <= len(maze) and x < len(maze[y - 1]) and (maze[y - 1][x] & 4):
                    row.append(Tile.WALL)
                else:
                    row.append(Tile.FLOOR)

            elif tx % 2 == 0 and ty % 2 == 1:
                if tx == 0 or tx == 2 * len(maze[0]):
                    row.append(Tile.WALL)
                # Internal vertical wall: check EAST wall of cell on the left.
                elif y < len(maze) and 0 < x <= len(maze[y]) and (maze[y][x - 1] & 2):
                    row.append(Tile.WALL)
                else:
                    row.append(Tile.FLOOR)

            else:
                row.append(Tile.CORNER)

        tile_map.append(row)
    print(tile_map[0])
    return tile_map

def tiles_positions(maze):
    x_positions = []
    x = 0

    for tx in range(2 * len(maze[0]) + 1):
        x_positions.append(x)
        x += WALL_SIZE if tx % 2 == 0 else FLOOR_SIZE

    y_positions = []
    y = 0

    for ty in range(2 * len(maze) + 1):
        y_positions.append(y)
        y += WALL_SIZE if ty % 2 == 0 else FLOOR_SIZE
    return x_positions, y_positions

def pixels_to_tile(pos_x, pos_y, x_positions, y_positions):
    tile_x = 0
    for i in range(len(x_positions)):
        if pos_x < x_positions[i]:
            break
        tile_x = i

    tile_y = 0
    for i in range(len(y_positions)):
        if pos_y < y_positions[i]:
            break
        tile_y = i

    return tile_x, tile_y

def corner_code(tile_map, ty, tx):
    bits = (
        (-1, 0, 1),  # N
        (0, 1, 2),   # E
        (1, 0, 4),   # S
        (0, -1, 8),  # W
    )
    max_y = len(tile_map)
    max_x = len(tile_map[0]) if max_y else 0

    code = 0
    for dy, dx, bit in bits:
        ny = ty + dy
        nx = tx + dx
        if 0 <= ny < max_y and 0 <= nx < max_x and tile_map[ny][nx] == Tile.WALL:
            code |= bit
    return code


def draw_maze(surface, tile_map, maze):
    x_positions, y_positions = tiles_positions(maze)

    for ty in range(len(tile_map)):
        for tx in range(len(tile_map[0])):

            x = tx // 2
            y = ty // 2

            x_start = x_positions[tx]
            y_start = y_positions[ty]

            if tile_map[ty][tx] == Tile.WALL:
                if ty % 2 == 0:
                    pygame.draw.line(surface, Color.BLUE, (x_start, y_start), (x_start + FLOOR_SIZE, y_start), width=2)
                    pygame.draw.line(surface, Color.BLUE, (x_start, y_start + WALL_SIZE), (x_start + FLOOR_SIZE, y_start + WALL_SIZE), width=2)
                if tx % 2 == 0:
                    pygame.draw.line(surface, Color.BLUE, (x_start, y_start), (x_start, y_start + FLOOR_SIZE), width=2)
                    pygame.draw.line(surface, Color.BLUE, (x_start + WALL_SIZE, y_start), (x_start + WALL_SIZE, y_start + FLOOR_SIZE), width=2)

            if tile_map[ty][tx] == Tile.CORNER:
                code = corner_code(tile_map, ty, tx)
                CORNER_DRAWER.get(code, lambda s, x, y: None)(surface, x_start, y_start)

            if tile_map[ty][tx] == Tile.FLOOR and maze[y][x] == 15:
                print(maze[y][x])
                pygame.draw.rect(surface, Color.CYAN, pygame.Rect((x_start, y_start), (FLOOR_SIZE, FLOOR_SIZE)), border_radius=7)

if __name__ == "__main__":
    pygame.init()

    maze_w = WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * WIDTH
    maze_h = WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * HEIGHT
    maze_surface = pygame.Surface((maze_w + 1, maze_h + 1))

    maze_gen = MazeGenerator(size=(HEIGHT, WIDTH))
    maze_gen.generate(seed=42)
    tile_map = to_tile_map(maze_gen.maze)
    draw_maze(maze_surface, tile_map, maze_gen.maze)

    screen = pygame.display.set_mode((maze_w, maze_h))
    clock = pygame.time.Clock()
    pacman = Pacman()

    running = True
    dt = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(maze_surface, (0, 0))
        screen.blit(pacman.image, pacman.rect.topleft)
        pacman.next_direction = pygame.key.get_pressed()
        pacman.update(maze_gen.maze)
        pygame.display.flip()
        dt = clock.tick(60)


    pygame.quit()
