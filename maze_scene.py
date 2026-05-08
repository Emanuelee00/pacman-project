from characters import Pacman, Blinky, Clyde, Inky, Pinky
import pygame
from typing import Optional
import maze_drawing
from mazegenerator.mazegenerator import MazeGenerator
import os
from pygame import Surface
from setting_manager import SettingManager
from settings import Tile, HEIGHT, WIDTH, FLOOR_SIZE, WALL_SIZE, COLOR
CELL_SIZE = 40
WS = 10
TS = CELL_SIZE + WS * 2
TS_D1 = TS + 1
TS_D2 = TS + 3
screen_size = SettingManager.get_screen_size()
maze_gen = MazeGenerator((15, 15), seed=42)
maze = maze_gen.maze


class MainScene():

    @staticmethod
    def run_scene_main():
        pygame.init()

        maze_w = WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * WIDTH
        maze_h = WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * HEIGHT
        maze_surface = pygame.Surface((maze_w + 1, maze_h + 1))
        pacgum_surface = pygame.Surface((maze_w + 1, maze_h + 1), pygame.SRCALPHA)
        maze_offset = ((screen_size[0] - maze_w) // 2, (screen_size[1] - maze_h) // 2)

        screen1 = pygame.display.set_mode(screen_size)

        clock = pygame.time.Clock()
        blinky = Blinky()
        pinky  = Pinky()
        inky   = Inky()
        clyde  = Clyde()

        pacman1 = Pacman()
        running = True

        tile_map = maze_drawing.to_tile_map(maze)
        x_positions, y_positions = maze_drawing.tiles_positions()

        pacgum_img = pygame.image.load(
            os.path.join(
                os.path.dirname(__file__),
                "characters/pacman-art/other/dot.png",
                )
            )
        pacgum_img = pygame.transform.scale(pacgum_img, (10, 10))
        MainScene.surface_maze(maze, maze_surface)
        MainScene.surface_pacgum(pacgum_img, maze, pacgum_surface)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pacman1.next_direction = pygame.key.get_pressed()
            pacman1.update(maze, tile_map, x_positions, y_positions)

            screen1.fill("black")
            screen1.blit(maze_surface, maze_offset)
            screen1.blit(pacgum_surface, maze_offset)
            for y in range(len(maze)):
                for x in range(len(maze[y])):
                    cx = x * (WALL_SIZE + FLOOR_SIZE) + WALL_SIZE + FLOOR_SIZE // 2 + maze_offset[0]
                    cy = y * (WALL_SIZE + FLOOR_SIZE) + WALL_SIZE + FLOOR_SIZE // 2 + maze_offset[1]
                    pygame.draw.circle(screen1, "red", (cx, cy), 3)
                    if x + 1 < len(maze[y]) and not (maze[y][x] & 2):
                        nx = (x + 1) * (WALL_SIZE + FLOOR_SIZE) + WALL_SIZE + FLOOR_SIZE // 2 + maze_offset[0]
                        pygame.draw.line(screen1, "red", (cx, cy), (nx, cy), 2)
                    if y + 1 < len(maze) and not (maze[y][x] & 4):
                        ny = (y + 1) * (WALL_SIZE + FLOOR_SIZE) + WALL_SIZE + FLOOR_SIZE // 2 + maze_offset[1]
                        pygame.draw.line(screen1, "red", (cx, cy), (cx, ny), 2)
            MainScene.display(screen1, blinky)
            MainScene.display(screen1, pinky)
            MainScene.display(screen1, inky)
            MainScene.display(screen1, clyde)
            screen1.blit(pacman1.image, (pacman1.pos_x + maze_offset[0], pacman1.pos_y + maze_offset[1]))

            pygame.display.flip()
            clock.tick(120)

        pygame.quit()

    @staticmethod
    def movement(pacman: Pacman, direction: str) -> str:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pacman.pos_x -= 3
            direction = "left"
        elif keys[pygame.K_RIGHT]:
            pacman.pos_x += 3
            direction = "right"
        elif keys[pygame.K_UP]:
            pacman.pos_y -= 3
            direction = "up"
        elif keys[pygame.K_DOWN]:
            pacman.pos_y += 3
            direction = "down"
        return direction

    @staticmethod
    def display(screen: Surface,
                name: Blinky | Pinky | Inky | Clyde):
        if isinstance(name, Blinky):
            name.update()
            screen.blit(name.image, (20, 20))
        elif isinstance(name, Pinky):
            name.update()
            screen.blit(name.image, (20, 70))
        elif isinstance(name, Inky):
            name.update()
            screen.blit(name.image, (70, 20))
        elif isinstance(name, Clyde):
            name.update()
            screen.blit(name.image, (70, 70))

    @staticmethod
    def surface_maze(maze: list[list[int]], maze_surface: Surface):
        maze_surface.fill("black")
        maze_drawing.draw_maze(maze_surface, maze_drawing.to_tile_map(maze))

    @staticmethod
    def surface_pacgum(img_pacgum: Surface, maze: list[list[int]], pacgum_surface: Surface):
        pacgum_surface.fill((0, 0, 0, 0))
        cell = WALL_SIZE + FLOOR_SIZE
        half_w = img_pacgum.get_width() // 2
        half_h = img_pacgum.get_height() // 2
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] != 15:
                    cx = x * cell + WALL_SIZE + FLOOR_SIZE // 2
                    cy = y * cell + WALL_SIZE + FLOOR_SIZE // 2
                    pacgum_surface.blit(img_pacgum, (cx - half_w, cy - half_h))

    

if __name__ == "__main__":
    pygame.init()

    maze_w = WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * WIDTH
    maze_h = WALL_SIZE + (WALL_SIZE + FLOOR_SIZE) * HEIGHT
    maze_surface = pygame.Surface((maze_w + 1, maze_h + 1))

    maze_gen = MazeGenerator(size=(HEIGHT, WIDTH))
    maze_gen.generate(seed=42)
    tile_map = maze_drawing.to_tile_map(maze_gen.maze)
    maze_drawing.draw_maze(maze_surface, tile_map)

    screen = pygame.display.set_mode((maze_w, maze_h))
    clock = pygame.time.Clock()
    pacman = Pacman()

    running = True
    dt = 0

    x_positions, y_positions = maze_drawing.tiles_positions()
    for x, y in zip(x_positions, y_positions):
        print(f"({x},{y})")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(maze_surface, (0, 0))
        screen.blit(pacman.image, (pacman.pos_x, pacman.pos_y))
        pacman.next_direction = pygame.key.get_pressed()
        pacman.update(tile_map, x_positions, y_positions)
        pygame.display.flip()
        dt = clock.tick(60)


    pygame.quit()
