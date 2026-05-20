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
from scenes.scene import Scene
from maze_drawing import draw_maze, to_tile_map
from pathlib import Path
from spritesheet import Spritesheet
from characters.pacman import Pacman

class PlayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.size = (
            self.game.levels[self.game.current_level].height,
            self.game.levels[self.game.current_level].width
            )
        print(f"size = {self.size}")
        maze_h, maze_w = self.size
        tilemap_w = WALL_SIZE + CELL_SIZE * maze_w
        tilemap_h = WALL_SIZE + CELL_SIZE * maze_h
        self.game_canvas = pygame.Surface((
            tilemap_w + 2 * OFFSET_X, tilemap_h + 2 * OFFSET_Y)
            )

        current_dir = Path(__file__).parent
        spritesheet_maze = Spritesheet(current_dir.parent / "maze_tiles.png")

        print("hello")
        self.maze_gen = MazeGenerator(size=self.size, seed=self.game.seed)
        tile_map = to_tile_map(self.maze_gen.maze)
        self.maze = self.maze_gen.maze

        spritesheet_pacman = Spritesheet(current_dir.parent / "assets" / "pacman_sprites.png")
        self.pacman = Pacman(self.maze, spritesheet_pacman)
        draw_maze(self.game_canvas, tile_map, self.maze, spritesheet_maze)
        self.missiles_group = pygame.sprite.Group()

    def enter_scene(self):
        super().enter_scene()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_scene()
                if event.key == pygame.K_SPACE:
                    self.game.pacman.shoot(self.missiles_group)

    def update(self) -> None:
        self.missiles_group.update()

    def render(self, surface) -> None:
        surface.fill((0, 0, 0))
        surface.blit(self.game_canvas, (0, 0))
        self.missiles_group.draw(surface)
        surface.blit(self.pacman.image, (0, 0))