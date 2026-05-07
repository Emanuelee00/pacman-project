import pygame

import pygame.gfxdraw

from mazegenerator.mazegenerator import MazeGenerator

import math

from enum import IntEnum

from characters.character import Pacman





class Tile(IntEnum):

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

SCREEN_SIZE = (WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * WIDTH + 300, WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * HEIGHT +300) 



maze_gen = MazeGenerator((HEIGHT, WIDTH), seed=42)

maze = maze_gen.maze



for maze_row in maze:

    print(maze_row)



def to_tile_map(maze) -> list:

    tile_map = []



    for ty in range(2 * HEIGHT + 1):

        row = []

        for tx in range(2 * WIDTH + 1):

            x = tx // 2

            y = ty // 2



            if tx % 2 == 1 and ty % 2 == 1:

                row.append(Tile.FLOOR)



            elif tx % 2 == 1 and ty % 2 == 0:

                if ty == 0 or ty == 2 * HEIGHT:

                    row.append(Tile.WALL)

                # Internal horizontal wall: check SOUTH wall of cell above.

                elif 0 < y <= len(maze) and x < len(maze[y - 1]) and (maze[y - 1][x] & 4):

                    row.append(Tile.WALL)

                else:

                    row.append(Tile.FLOOR)



            elif tx % 2 == 0 and ty % 2 == 1:

                if tx == 0 or tx == 2 * WIDTH:

                    row.append(Tile.WALL)

                # Internal vertical wall: check EAST wall of cell on the left.

                elif y < len(maze) and 0 < x <= len(maze[y]) and (maze[y][x - 1] & 2):

                    row.append(Tile.WALL)

                else:

                    row.append(Tile.FLOOR)



            else:

                row.append(Tile.CORNER)



        tile_map.append(row)



    return tile_map



def tiles_positions():

    x_positions = []

    x = 0



    for tx in range(2 * WIDTH + 1):

        x_positions.append(x)

        x += WALL_SIZE if tx % 2 == 0 else FLOOR_SIZE



    y_positions = []

    y = 0



    for ty in range(2 * HEIGHT + 1):

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



def draw_corner_tile(x_start, y_start, code, screen):

    # Draw in terms of N/E/S/W branches from the center.

    if code == 1:

        for dr in range(2):

            pygame.gfxdraw.arc(screen, x_start + WALL_SIZE // 2, y_start, (WALL_SIZE // 2) - dr, 0, 180, (0, 0, 255))

    if code == 2:

        for dr in range(2):

            pygame.gfxdraw.arc(screen, x_start + WALL_SIZE, y_start + WALL_SIZE // 2, (WALL_SIZE // 2) - dr, 90, 270, (0, 0, 255))

    if code == 3: # SW corner

        for dr in range(2):

            pygame.gfxdraw.arc(screen, x_start + WALL_SIZE, y_start, WALL_SIZE - dr, 90, 180, (0, 0, 255))

    if code == 4:

        for dr in range(2):

            pygame.gfxdraw.arc(screen, x_start + WALL_SIZE // 2, y_start + WALL_SIZE, (WALL_SIZE // 2) - dr, 180, 360, (0, 0, 255))

    if code == 5:

        pygame.draw.line(screen, "blue", (x_start, y_start), (x_start, y_start + WALL_SIZE), width=2)

        pygame.draw.line(screen, "blue", (x_start + WALL_SIZE, y_start), (x_start + WALL_SIZE, y_start + WALL_SIZE), width=2)

    if code == 6: # NW corner

        for dr in range(2):

            pygame.gfxdraw.arc(screen, x_start + WALL_SIZE, y_start + WALL_SIZE, WALL_SIZE - dr, 180, 270, (0, 0, 255))

    if code == 7:

        pygame.draw.line(screen, "blue", (x_start, y_start), (x_start, y_start + WALL_SIZE), width=2)

    if code == 8:

        for dr in range(2):

            pygame.gfxdraw.arc(screen, x_start, y_start + WALL_SIZE // 2, (WALL_SIZE // 2) - dr, 270, 450, (0, 0, 255))

    if code == 9: # SE corner

        for dr in range(2):

            pygame.gfxdraw.arc(screen, x_start, y_start, WALL_SIZE - dr, 0, 90, (0, 0, 255))

    if code == 10:

        pygame.draw.line(screen, "blue", (x_start, y_start), (x_start + WALL_SIZE, y_start), width=2)

        pygame.draw.line(screen, "blue", (x_start, y_start + WALL_SIZE), (x_start + WALL_SIZE, y_start + WALL_SIZE), width=2)

    if code == 11:

        pygame.draw.line(screen, "blue", (x_start, y_start + WALL_SIZE), (x_start + WALL_SIZE, y_start + WALL_SIZE), width=2)

    if code == 12: #NE corner

        for dr in range(2):

            pygame.gfxdraw.arc(screen, x_start, y_start + WALL_SIZE, WALL_SIZE - dr, 270, 360, (0, 0, 255))

    if code == 13:

        pygame.draw.line(screen, "blue", (x_start + WALL_SIZE, y_start), (x_start + WALL_SIZE, y_start + WALL_SIZE), width=2)

    if code == 14:

        pygame.draw.line(screen, "blue", (x_start, y_start), (x_start + WALL_SIZE, y_start), width=2)



def print_maze(tile_map, screen):

    x_positions, y_positions = tiles_positions()



    for ty in range(2 * HEIGHT + 1):

        for tx in range(2 * WIDTH + 1):



            x = tx // 2

            y = ty // 2



            x_start = x_positions[tx]

            y_start = y_positions[ty]



            if tile_map[ty][tx] == Tile.WALL:

                if ty % 2 == 0:

                    pygame.draw.line(screen, "blue", (x_start, y_start), (x_start + FLOOR_SIZE, y_start), width=2)

                    pygame.draw.line(screen, "blue", (x_start, y_start + WALL_SIZE), (x_start + FLOOR_SIZE, y_start + WALL_SIZE), width=2)

                if tx % 2 == 0:

                    pygame.draw.line(screen, "blue", (x_start, y_start), (x_start, y_start + FLOOR_SIZE), width=2)

                    pygame.draw.line(screen, "blue", (x_start + WALL_SIZE, y_start), (x_start + WALL_SIZE, y_start + FLOOR_SIZE), width=2)



            if tile_map[ty][tx] == Tile.CORNER:

                code = corner_code(tile_map, ty, tx)

                draw_corner_tile(x_start, y_start, code, screen)





tile_map = to_tile_map(maze)

# print("Tile map:")

# for tile_row in tile_map:

#     print(tile_row)
if __name__ == "__main__":
    from pacman_movements import movement
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)

    clock = pygame.time.Clock()

    pacman = Pacman()

    running = True

    dt = 0

    pos_x = 50

    pos_y = 50

    direction = ""

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False



        screen.fill("black")

        print_maze(tile_map, screen)



        pos_x, pos_y, direction = movement(pos_x, pos_y, direction)

        print(pos_x)

        print(pos_y)

        pacman.update(direction)

        screen.blit(pacman.image, (pos_x, pos_y))



        # print(f"x={x}, y={y}, TS={TS}")

        # print(f"res={curr_pos & 1}")





        pygame.display.flip()

        dt = clock.tick(60)





    pygame.quit()