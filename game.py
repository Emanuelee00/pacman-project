import pygame
from settings import SCREEN_SIZE, HEIGHT, WIDTH, TILEMAP_HEIGHT, TILEMAP_WIDTH
from mazegenerator.mazegenerator import MazeGenerator
from maze_drawing import to_tile_map, draw_maze
from characters.ghosts import Inky, Blinky, Pinky, Clyde
from characters.pacman import Pacman
from pacgum import Pacgum, PacgumManager


class Game:
    def __init__(self) -> None:
        pygame.init()

        self._screen = pygame.display.set_mode(SCREEN_SIZE)

        maze_gen = MazeGenerator(size=(WIDTH, HEIGHT))
        maze_gen.generate(seed=42)
        self.maze = maze_gen.maze

        tile_map = to_tile_map(maze_gen.maze)
        self.maze_surface = pygame.Surface((TILEMAP_WIDTH + 2, TILEMAP_HEIGHT + 2))
        draw_maze(self.maze_surface, tile_map, self.maze)

        self.pacgums_group = PacgumManager(maze_gen.maze).group
        self.pacman = Pacman()
        self.ghost = Blinky()
        self.pacman.respawn(self.maze)
        self.ghost.respawn(self.maze)

        self._running = True
        self._clock = pygame.time.Clock()

    def run(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            self.pacman.next_direction = pygame.key.get_pressed()
            self.pacman.update(self.maze)
            self.ghost.update(self.maze)

            hits = pygame.sprite.spritecollide(self.pacman, self.pacgums_group, True)

            self._screen.fill((0, 0, 0))
            self._screen.blit(self.maze_surface, (0, 0))
            self.pacgums_group.draw(self._screen)
            self._screen.blit(self.pacman.image, self.pacman.rect)
            self._screen.blit(self.ghost.image, self.ghost.rect)

            pygame.display.flip()
            dt = self._clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    Game().run()
