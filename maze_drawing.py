import pygame
import pygame.gfxdraw
from settings import Tile, HEIGHT, WIDTH, FLOOR_SIZE, WALL_SIZE, Color
from mazegenerator.mazegenerator import MazeGenerator
from characters.pacman import Pacman
from maze_spritesheet import MazeSpritesheet, Tiles
import pathlib


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
                elif 0 < y <= len(maze) and x < len(maze[y - 1]) and (maze[y - 1][x] & 4):
                    row.append(Tile.WALL)
                else:
                    row.append(Tile.FLOOR)

            elif tx % 2 == 0 and ty % 2 == 1:
                if tx == 0 or tx == 2 * len(maze[0]):
                    row.append(Tile.WALL)
                elif y < len(maze) and 0 < x <= len(maze[y]) and (maze[y][x - 1] & 2):
                    row.append(Tile.WALL)
                else:
                    row.append(Tile.FLOOR)

            else:
                row.append(Tile.CORNER)

        tile_map.append(row)
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


def draw_maze(surface, tile_map, maze, spritesheet):
    x_positions, y_positions = tiles_positions(maze)

    for ty in range(len(tile_map)):
        for tx in range(len(tile_map[0])):

            x = tx // 2
            y = ty // 2

            x_start = x_positions[tx]
            y_start = y_positions[ty]

            if tile_map[ty][tx] == Tile.WALL:
                if ty % 2 == 0:
                    sprite = spritesheet.get_sprite(*Tiles[17])
                if tx % 2 == 0:
                    sprite = spritesheet.get_sprite(*Tiles[16])
                surface.blit(sprite, (x_start, y_start))

            if tile_map[ty][tx] == Tile.CORNER:
                code = corner_code(tile_map, ty, tx)
                if code == 0:
                    continue
                sprite = spritesheet.get_sprite(*Tiles[code])
                surface.blit(sprite, (x_start, y_start))

            if tile_map[ty][tx] == Tile.FLOOR and maze[y][x] == 15:
                pygame.draw.rect(surface, Color.CYAN, pygame.Rect((x_start - 4, y_start - 4), (FLOOR_SIZE + 8, FLOOR_SIZE + 8)), border_radius=5)


if __name__ == "__main__":
    pygame.init()

    maze_w = WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * WIDTH
    maze_h = WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * HEIGHT
    maze_surface = pygame.Surface((maze_w + 1, maze_h + 1))

    maze_gen = MazeGenerator(size=(HEIGHT, WIDTH))
    maze_gen.generate(seed=42)
    tile_map = to_tile_map(maze_gen.maze)

    current_dir = pathlib.Path(__file__).parent
    spritesheet_image = pygame.image.load(current_dir / "maze_tiles11.png")
    spritesheet = MazeSpritesheet(spritesheet_image)
    draw_maze(maze_surface, tile_map, maze_gen.maze, spritesheet)

    screen = pygame.display.set_mode((maze_w, maze_h))
    clock = pygame.time.Clock()
    pacman = Pacman(maze_gen.maze)

    print(corner_code(tile_map, 5, 4))
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
        pacman.update()
        pygame.display.flip()
        dt = clock.tick(60)

    pygame.quit()
