import pygame
from game import Game
from settings import (
     SCREEN_WIDTH,
     SCREEN_HEIGHT,
)
from parser import GameConfig, load_highscores, LevelConfig

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    config = GameConfig(
        highscore_filename="highscores.json",
        lives=3,
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
        seed=42,
        level_max_time=90,
        levels=[
            LevelConfig(
                id=1,
                width=15,
                height=15,
                pacgum_count=42,
                super_pacgum_count=4
            )
        ]
    )
    game = Game(config)
    game.run()
