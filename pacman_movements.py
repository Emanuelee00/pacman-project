from characters import Pacman, Blinky, Clyde, Inky, Pinky
import pygame
from typing import Optional
import test
from mazegenerator.mazegenerator import MazeGenerator



CELL_SIZE = 40
WS = 10
TS = CELL_SIZE + WS * 2
TS_D1 = TS + 1
TS_D2 = TS + 3
screen_size = (TS * 11, TS * 11)

maze_gen = MazeGenerator((10, 10), seed=42)
maze = maze_gen.maze

def movement(pos_x, pos_y, direction):
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pos_x -= 3
        direction = "left"
    elif keys[pygame.K_RIGHT]:
        pos_x += 3
        direction = "right"
    elif keys[pygame.K_UP]:
        pos_y -= 3
        direction = "up"
    elif keys[pygame.K_DOWN]:
        pos_y += 3
        direction = "down"

    return (pos_x, pos_y, direction)

def display(name: Pacman | Blinky | Pinky | Inky | Clyde, direction: Optional[str] = None):
    if isinstance(name,Pacman) and direction:
        name.update(direction)
        screen.blit(pacman1.image, (pos_x, pos_y))
    elif not direction and isinstance(name,Blinky):
        name.update()
        screen.blit(name.image, (20, 20))
    elif not direction and isinstance(name,Pinky):
        name.update()
        screen.blit(name.image, (20, 70))
    elif not direction and isinstance(name,Inky):
        name.update()
        screen.blit(name.image, (70, 20))
    elif not direction and isinstance(name,Clyde):
        name.update()
        screen.blit(name.image, (70, 70))


if __name__ == "__main__":


    pygame.init()

    screen = pygame.display.set_mode((1000, 1000))
    clock = pygame.time.Clock()
    blinky = Blinky()
    pinky  = Pinky()
    inky   = Inky()
    clyde  = Clyde()

    pacman1 = Pacman()
    pos_x = 100
    pos_y = 100
    running = True
    direction = "right"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pos_x, pos_y, direction = movement(pos_x, pos_y, direction)

        screen.fill("black")
        display(pacman1, direction)
        display(blinky)
        display(pinky)
        display(inky)
        display(clyde)

        for y in range(len(maze)):
            for x in range(len(maze[y])):
                curr_pos = maze[y][x]
                test.ft_func(curr_pos, screen, x, y, TS)

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()