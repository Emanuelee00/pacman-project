from characters import Pacman, Blinky, Clyde, Inky, Pinky
import pygame
from typing import Optional
import test2
from mazegenerator.mazegenerator import MazeGenerator
import os
from pygame import Surface
from setting_manager import SettingManager

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

        maze_w = test2.WALL_SIZE + (test2.WALL_SIZE + test2.FLOOR_SIZE) * test2.WIDTH
        maze_h = test2.WALL_SIZE + (test2.WALL_SIZE + test2.FLOOR_SIZE) * test2.HEIGHT
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
        direction = "right"

        pacgum_img = pygame.image.load(
            os.path.join(
                os.path.dirname(__file__), 
                "characters/pacman-art/other/dot.png",
                )
            )
        pacgum_img = pygame.transform.scale(pacgum_img, (50, 50))
        MainScene.surface_maze(maze, maze_surface)
        MainScene.surface_pacgum(pacgum_img, maze, pacgum_surface)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            direction = MainScene.movement(pacman1, direction)

            screen1.fill("black")
            screen1.blit(maze_surface, maze_offset)
            screen1.blit(pacgum_surface, maze_offset)
            MainScene.display(screen1, blinky)
            MainScene.display(screen1, pinky)
            MainScene.display(screen1, inky)
            MainScene.display(screen1, clyde)
            MainScene.display(screen1, pacman1, direction)
        

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
                name: Pacman | Blinky | Pinky | Inky | Clyde,
                direction: Optional[str] = None):
        if isinstance(name, Pacman) and direction:
            name.update(direction)
            screen.blit(name.image, (name.pos_x, name.pos_y))
        elif isinstance(name, Blinky):
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
        test2.print_maze(test2.to_tile_map(maze), maze_surface)

    @staticmethod
    def surface_pacgum(img_pacgum: Surface, maze: list[list[int]], pacgum_surface: Surface):
        pacgum_surface.fill((0, 0, 0, 0))
        cell = test2.WALL_SIZE + test2.FLOOR_SIZE
        half_w = img_pacgum.get_width() // 2
        half_h = img_pacgum.get_height() // 2
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] != 15:
                    cx = x * cell + test2.WALL_SIZE + test2.FLOOR_SIZE // 2
                    cy = y * cell + test2.WALL_SIZE + test2.FLOOR_SIZE // 2
                    pacgum_surface.blit(img_pacgum, (cx - half_w, cy - half_h))

    