import pygame
from mazegenerator.mazegenerator import MazeGenerator
from characters import Pacman, Blinky, Clyde, Inky, Pinky
import pygame
from typing import Optional

CELL_SIZE = 40
WS = 10
TS = CELL_SIZE + WS * 2
TS_D1 = TS + 1
TS_D2 = TS + 3
screen_size = (TS * 11, TS * 11)

maze_gen = MazeGenerator((10, 10), seed=42)
maze = maze_gen.maze

for maze_row in maze:
    print(maze_row)

def ft_func(curr_pos, screen, x:int, y:int, Ts:int) -> None:
    if curr_pos & 1:
        pygame.draw.line(screen, "blue", (x * Ts, y * Ts), ((x * Ts) + Ts, y * Ts), width=10)
        # pygame.draw.line(screen, "black", (x * Ts, y * Ts), ((x * Ts) + Ts, y * Ts), width=5)
    if curr_pos & 2:
        pygame.draw.line(screen, "yellow", ((x * Ts) + Ts, y * Ts), ((x * Ts) + Ts, (y * Ts) + Ts), width=10)
        pygame.draw.line(screen, "black", ((x * Ts) + Ts, y * Ts), ((x * Ts) + Ts, (y * Ts) + Ts), width=5)
        pygame.draw.line(screen, "yellow", (x * Ts, (y * Ts) + Ts), ((x * Ts) + Ts, (y * Ts) + Ts), width=10)
        pygame.draw.line(screen, "black", (x * Ts, (y * Ts) + Ts), ((x * Ts) + Ts, (y * Ts) + Ts), width=5)
    if curr_pos & 8:
        pygame.draw.line(screen, "YELLOW", (x * Ts, y * Ts), (x * Ts, (y * Ts) + Ts), width=10)
        pygame.draw.line(screen, "black", (x * Ts, y * Ts), (x * Ts, (y * Ts) + Ts), width=5)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")


        for y in range(len(maze)):
            for x in range(len(maze[y])):

                curr_pos = maze[y][x]
                ft_func(curr_pos, screen, x, y, TS)


                # print(f"x={x}, y={y}, TS={TS}")
                # print(f"res={curr_pos & 1}")


        pygame.display.flip()
        dt = clock.tick(60)

    pygame.quit()