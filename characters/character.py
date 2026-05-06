import pygame
import os
import pdb
from pygame import surface
from typing import Optional
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walk_anim = []

    SIZE = (50, 50)

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
        self.frame_slower = 0

        self.animation = {
            "down" : self.load_anim("pacman-down"),
            "left" : self.load_anim("pacman-left"),
            "right" : self.load_anim("pacman-right"),
            "up" : self.load_anim("pacman-up")
            }
        print(self.animation)
        self.image = self.animation["right"][0]  # già scalata da load_anim

    def update(self, direction: str):
        if direction:
            frame = self.animation[direction]
            self.frame_slower += 0.05

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