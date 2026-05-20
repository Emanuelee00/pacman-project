from pathlib import Path
import pygame
from menu_scene import MenuScene
from spritesheet import Spritesheet
from settings import (
    HEIGHT,
    WIDTH,
    WALL_SIZE,
    CELL_SIZE,
    OFFSET_X,
    OFFSET_Y,
    CHEAT_LIVES,
    UNCHEAT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    FPS
)
from mazegenerator.mazegenerator import MazeGenerator
from maze_drawing import to_tile_map, draw_maze
from characters.ghosts import Inky, Blinky, Pinky, Clyde
from characters.pacman import Pacman
from pacgum import Pacgum, PacgumManager
from parser import GameConfig, load_highscores
from pygame import Surface


class Game:
    def __init__(self, config: GameConfig | None = None) -> None:
        pygame.init()

        if config:
            self._set_config(config)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        self.scenes_stack = []
        self._load_scenes()
        self._load_assets()
        self.current_level = 0
        self.current_dir = Path(__file__).parent
        # self.lives = 1
        # self.points_per_pacgum = 10
        # self.points_per_super_pacgum = 50
        # self.points_per_ghost = 200
        # self.seed = 43
        # self.level_max_time = None
        # self.levels = None
        # self.size = (HEIGHT, WIDTH)
        # self.score = 0
        # self._key_buffer = []
        # try:
        #     hs = load_highscores()
        #     self.high_score = max((e.score for e in hs.scores), default=0)
        # except Exception:
        #     self.high_score = 0

        # if config:
        #     self._set_config(config)


        # maze_gen = MazeGenerator(size=self.size, seed=self.seed)
        # self.maze = maze_gen.maze

        # tile_map = to_tile_map(maze_gen.maze)
        # self.maze_surface = pygame.Surface((tilemap_w + 2, tilemap_h + 2))
        # current_dir = pathlib.Path(__file__).parent
        # spritesheet = Spritesheet(current_dir / "maze_tiles.png")

        # draw_maze(self.maze_surface, tile_map, self.maze, spritesheet)
        # self.game_surface = pygame.Surface((tilemap_w + 2, tilemap_h + 2))

        # ghosts_spritesheet = Spritesheet(current_dir / "assets" / "ghosts_sprites.png")
        # pacman_spritesheet = Spritesheet(current_dir / "assets" / "pacman_sprites.png")
        # self.pacgums_group = PacgumManager(maze_gen.maze).group
        # self.pacman = Pacman(self.maze, pacman_spritesheet)
        # self.blinky = Blinky(self.maze, self.pacman, ghosts_spritesheet)
        # self.pinky = Pinky(self.maze, self.pacman, ghosts_spritesheet)
        # self.inky = Inky(self.maze, self.pacman, self.blinky, ghosts_spritesheet)
        # self.clyde = Clyde(self.maze, self.pacman, ghosts_spritesheet)

        # self.pacman.respawn()
        # self.blinky.respawn()
        # self.pinky.respawn()
        # self.inky.respawn()
        # self.clyde.respawn()

        # self._running = True
        # self._game_ended = False
        # self._clock = pygame.time.Clock()
        # self._start_time = pygame.time.get_ticks()
        # self._cheat_time = None
        # self._game_over_time = None

    def _set_config(self, config: GameConfig):
        self.lives = config.lives
        self.points_per_pacgum = config.points_per_pacgum
        self.points_per_super_pacgum = config.points_per_super_pacgum
        self.points_per_ghost = config.points_per_ghost
        self.seed = config.seed
        self.level_max_time = config.level_max_time
        self.levels = config.levels

    # def _display_info(self, milliseconds):
    #     font = pygame.font.SysFont("Arial", 18)
    #     screen_w = self.screen.get_width()
    #     screen_h = self.screen.get_height()

    #     # Top left: 1UP + score
    #     self.screen.blit(font.render("POINTS", True, (Color.WHITE)), (OFFSET_X, 8))
    #     self.screen.blit(font.render(str(self.score), True, (Color.WHITE)), (OFFSET_X, 28))

    #     # Top center: HIGH SCORE
    #     hs_label = font.render("HIGH SCORE", True, (Color.WHITE))
    #     hs_val = font.render(str(self.high_score), True, (Color.WHITE))
    #     cx = screen_w // 2
    #     self.screen.blit(hs_label, (cx - hs_label.get_width() // 2, 8))
    #     self.screen.blit(hs_val, (cx - hs_val.get_width() // 2, 28))

    #     # Top right: TIME
    #     elapsed = (pygame.time.get_ticks() - self._start_time) // 1000
    #     time_label = font.render("TIME", True, Color.WHITE)
    #     time_val = font.render(f"{elapsed // 60:02}:{elapsed % 60:02}", True, Color.WHITE)
    #     self.screen.blit(time_label, (screen_w - OFFSET_X - time_label.get_width(), 8))
    #     self.screen.blit(time_val, (screen_w - OFFSET_X - time_val.get_width(), 28))

    #     # Bottom left: life icons (lives - 1, current life not shown)
    #     icon_y = screen_h - OFFSET_Y // 2
    #     for i in range(self.lives):
    #         pygame.draw.circle(self.screen, (Color.YELLOW), (OFFSET_X + i * 30, icon_y), 10)

    #     # Cheat message: mostra per 3 secondi
    #     if self._cheat_time and pygame.time.get_ticks() - self._cheat_time < milliseconds:
    #         cheat_font = pygame.font.SysFont("Arial", 100)
    #         line1 = cheat_font.render("FOR THE", True, Color.YELLOW)
    #         line2 = cheat_font.render("FAMILY", True, Color.YELLOW)
    #         self.screen.blit(line1, (screen_w // 2 - line1.get_width() // 2, screen_h // 2 - line1.get_height()))
    #         self.screen.blit(line2, (screen_w // 2 - line2.get_width() // 2, screen_h // 2))
    #     else:
    #         self._cheat_time = None

    # def _display_game_over(self, milliseconds):
    #     if self._game_over_time is None:
    #         self._game_over_time = pygame.time.get_ticks()
    #     elapsed = pygame.time.get_ticks() - self._game_over_time
    #     if elapsed >= milliseconds:
    #         self._game_ended = True
    #         self._running = False
    #         return
    #     font = pygame.font.SysFont("Arial", 60)
    #     game_over = font.render("GAME OVER", True, Color.RED)
    #     screen_w = self.screen.get_width()
    #     screen_h = self.screen.get_height()
    #     self.screen.blit(game_over, (screen_w // 2 - game_over.get_width() // 2, screen_h // 2))

    def _load_scenes(self):
        self.menu_scene = MenuScene(self)
        self.scenes_stack.append(self.menu_scene)

    def _load_assets(self):
        pass

    def draw_text(self, surface, text, color, x, y):
        font = pygame.font.Font(self.current_dir / "assets" / "Pixel_Digivolve.otf", 30)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = x, y
        surface.blit(text_surface, text_rect)
        return text_rect

    def run(self):
        while self.running:

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            current_scene = self.scenes_stack[-1]
            current_scene.handle_events(events)
            current_scene.update()
            self.screen.fill((0, 0, 0))
            current_scene.render(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
                # if event.type == pygame.KEYDOWN:
                #     self._key_buffer.append(event.key)
                #     self._key_buffer = self._key_buffer[-max(len(CHEAT_LIVES), len(UNCHEAT)):]
                #     if self._key_buffer[-len(CHEAT_LIVES):] == CHEAT_LIVES:
                #         self._cheat_time = pygame.time.get_ticks()
                #         self.pacman.set_cheated()
                #     if self._key_buffer[-len(UNCHEAT):] == UNCHEAT:
                #         self.pacman.set_normal()


        #     self.pacman.next_direction = pygame.key.get_pressed()
        #     self.pacman.update()
        #     self.blinky.update()
        #     self.pinky.update()
        #     self.inky.update()
        #     self.clyde.update()
        #     hits = pygame.sprite.spritecollide(self.pacman, self.pacgums_group, True)
        #     for hit in hits:
        #         if hit.is_super:
        #             self.score += self.points_per_super_pacgum
        #         else:
        #             self.score += self.points_per_pacgum

        #     if pygame.sprite.collide_rect(self.pacman, self.blinky):
        #         self.lives -= 1
        #         if self.lives > 0:
        #             self.pacman.respawn()

        #     self.game_surface.fill((0, 0, 0))
        #     self.game_surface.blit(self.maze_surface, (0, 0))
        #     self.pacgums_group.draw(self.game_surface)
        #     self.game_surface.blit(self.pacman.image, self.pacman.rect)
        #     self.game_surface.blit(self.blinky.image, self.blinky.rect)
        #     self.game_surface.blit(self.pinky.image, self.pinky.rect)
        #     self.game_surface.blit(self.inky.image, self.inky.rect)
        #     self.game_surface.blit(self.clyde.image, self.clyde.rect)
        #     self._screen.fill((0, 0, 0))

        #     self._screen.blit(self.game_surface, (OFFSET_X, OFFSET_Y))
        #     self._display_info(2000)
        #     if self.lives <= 0:
        #         self._display_game_over(2000)

        #     pygame.display.flip()
        #     self._clock.tick(60)
        # return self._game_ended


if __name__ == "__main__":
    Game().run()
    pygame.quit()
