from character import Character

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
        self.image = self.animation[0]
        self.rect = self.image.get_rect()

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
