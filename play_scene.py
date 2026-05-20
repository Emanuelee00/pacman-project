import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WALL_SIZE,
    CELL_SIZE,
    OFFSET_X,
    OFFSET_Y,
)
from mazegenerator.mazegenerator import MazeGenerator
from scene import Scene


class PlayScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.size = (
            self.game.levels[self.game.current_level].height,
            self.game.levels[self.game.current_level].width
            )
        maze_h, maze_w = self.size
        tilemap_w = WALL_SIZE + CELL_SIZE * maze_w
        tilemap_h = WALL_SIZE + CELL_SIZE * maze_h
        self.game_canvas = pygame.Surface((
            tilemap_w + 2 * OFFSET_X, tilemap_h + 2 * OFFSET_Y)
            )

        self.maze_gen = MazeGenerator(size=self.size, seed=self.game.seed)
        self.maze = self.maze_gen.maze

        

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass

    def update(self) -> None:
        pass