import pygame
import os
import pdb
from pygame import surface
from typing import Optional
from settings import Tile, Directions, SPEED, FLOOR_SIZE


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walk_anim = []

    SIZE = (45, 45)

    def load_anim(self, folder: str, image_name: Optional[str] = None):
        base = os.path.dirname(__file__)
        self.dir = self._get_dir(base, "pacman-art", folder)
        self.walk_anim = []
        if self.dir:
            if image_name:
                img = pygame.image.load(os.path.join(base, "pacman-art", folder, image_name))
                img = pygame.transform.scale(img, self.SIZE)
                self.walk_anim.append(img)
            else:
                for file in self.dir:
                    img = pygame.image.load(os.path.join(base, "pacman-art", folder, file))
                    img = pygame.transform.scale(img, self.SIZE)
                    self.walk_anim.append(img)
        return self.walk_anim

    @staticmethod
    def _get_dir(*args: str):
        try:
            dir = os.listdir(os.path.join(*args))
            for file in dir:
                if not file.endswith(".png"):
                    raise ValueError
            return dir
        except (FileNotFoundError, ValueError, TypeError) as e:
            print(e)
            return []


class Ghost(Character):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.animation = self.load_anim(f"ghosts/{self.name}")
        if not self.animation:
            raise ValueError(f"Ghost '{name}' not found — check the folder name")
        self.scared_anim = self.load_anim("ghosts/scared")
        self.scared = False
        self.frame_slower = 0
        self.pos_x = 0
        self.pos_y = 0

    def update(self):
        if self.scared:
            anim = self.scared_anim
            self.frame_slower += 0.05
        else:
            anim = self.animation
        self.frame_slower += 0.05
        if self.frame_slower >= len(anim):
            self.frame_slower = 0
        self.image = anim[int(self.frame_slower)]

    def move(self, pacman_pos: tuple):
        pass  # override in each subclass


class Blinky(Ghost):
    def __init__(self):
        super().__init__("blinky")

    def move(self, pacman_pos: tuple):
        pass  # insegue direttamente pacman


class Pinky(Ghost):
    def __init__(self):
        super().__init__("pinky")

    def move(self, pacman_pos: tuple, pacman_dir: str):
        pass  # anticipa di 4 tile


class Inky(Ghost):
    def __init__(self):
        super().__init__("inky")

    def move(self, pacman_pos: tuple, blinky_pos: tuple):
        pass  # comportamento misto


class Clyde(Ghost):
    def __init__(self):
        super().__init__("clyde")

    def move(self, pacman_pos: tuple):
        pass  # random quando lontano, scappa quando vicino



class Pacman(Character):
    def __init__(self):
        super().__init__()
        self.pos_x: int = 12
        self.pos_y: int = 12
        self.edges = {
            ''
        }
        self.direction: Directions = Directions.NONE
        self._next_direction: Directions = Directions.NONE

        self.frame_slower = 0
        self.animation = {
            Directions.UP : self.load_anim("pacman-up"),
            Directions.LEFT : self.load_anim("pacman-left"),
            Directions.RIGHT : self.load_anim("pacman-right"),
            Directions.DOWN : self.load_anim("pacman-down")
            }
        self.image = self.animation[Directions.RIGHT][0]
        self.radius = self.image.get_width() // 2

    def _can_move(self, tile_map, x_positions, y_positions):
        from maze_drawing import pixels_to_tile
        edge_x, edge_y = self.pos_x, self.pos_y
        if self.direction == Directions.LEFT:
            edge_y = self.pos_y + self.radius
        elif self.direction == Directions.RIGHT:
            edge_x = self.pos_x + 2 * self.radius
            edge_y = self.pos_y + self.radius
        elif self.direction == Directions.UP:
            edge_x = self.pos_x + self.radius
        elif self.direction == Directions.DOWN:
            edge_x = self.pos_x + self.radius
            edge_y = self.pos_y + 2 * self.radius

        tx, ty = pixels_to_tile(edge_x , edge_y, x_positions, y_positions)
        print(f"edge_x={edge_x}, edge_y={edge_y}")
        print(f"tx={tx}, ty={ty}")
        print(tile_map[ty][tx])
        return tile_map[ty][tx] == Tile.FLOOR

    @property
    def next_direction(self):
        return self._next_direction

    @next_direction.setter
    def next_direction(self, keys):
        if keys[pygame.K_LEFT]:
            self._next_direction = Directions.LEFT
        if keys[pygame.K_RIGHT]:
            self._next_direction = Directions.RIGHT
        if keys[pygame.K_UP]:
            self._next_direction = Directions.UP
        if keys[pygame.K_DOWN]:
            self._next_direction = Directions.DOWN

    def update(self, tile_map, x_positions, y_positions):

        self.direction = self._next_direction
        if self._can_move(tile_map, x_positions, y_positions):


            self.pos_x += self.direction.dx * SPEED
            self.pos_y += self.direction.dy * SPEED

        if self.direction != Directions.NONE:
            frame = self.animation[self.direction]

            self.frame_slower += 0.15
            if self.frame_slower >= len(frame):
                self.frame_slower = 0

            self.image = frame[int(self.frame_slower)]

if __name__ == "__main__":


    pygame.init()

    screen = pygame.display.set_mode((200, 200))
    clock = pygame.time.Clock()
    blinky = Blinky()
    pinky  = Ghost("pinky")
    inky   = Ghost("inky")
    clyde  = Ghost("clyde")

    pacman1 = Pacman()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")  # prima pulisci

        blinky.update()
        screen.blit(blinky.image, (50, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
