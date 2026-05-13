import pygame
from settings import HEIGHT, WIDTH, WALL_SIZE, CELL_SIZE, OFFSET_X, OFFSET_Y, CHEAT_LIVES, UNCHEAT, Color
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

        self.lives = 1
        self.points_per_pacgum = 10
        self.points_per_super_pacgum = 50
        self.points_per_ghost = 200
        self.seed = 42
        self.level_max_time = None
        self.levels = None
        self.size = (HEIGHT, WIDTH)
        self.score = 0
        self._key_buffer = []
        try:
            hs = load_highscores()
            self.high_score = max((e.score for e in hs.scores), default=0)
        except Exception:
            self.high_score = 0

        if config:
            self._set_config(config)

        h, w = self.size
        tilemap_w = WALL_SIZE + CELL_SIZE * w
        tilemap_h = WALL_SIZE + CELL_SIZE * h
        self._screen = pygame.display.set_mode((tilemap_w + 2 * OFFSET_X, tilemap_h + 2 * OFFSET_Y))

        maze_gen = MazeGenerator(size=self.size, seed=self.seed)
        self.maze = maze_gen.maze

        tile_map = to_tile_map(maze_gen.maze)
        self.maze_surface = pygame.Surface((tilemap_w + 2, tilemap_h + 2))
        draw_maze(self.maze_surface, tile_map, self.maze)
        self.game_surface = pygame.Surface((tilemap_w + 2, tilemap_h + 2))

        self.pacgums_group = PacgumManager(maze_gen.maze).group
        self.pacman = Pacman()
        self.ghost = Blinky()
        self.pacman.respawn(self.maze)
        self.ghost.respawn(self.maze)

        self._running = True
        self._game_ended = False
        self._clock = pygame.time.Clock()
        self._start_time = pygame.time.get_ticks()
        self._cheat_time = None
        self._game_over_time = None

    def _set_config(self, config: GameConfig):
        self.lives = config.lives
        self.points_per_pacgum = config.points_per_pacgum
        self.points_per_super_pacgum = config.points_per_super_pacgum
        self.points_per_ghost = config.points_per_ghost
        self.seed = config.seed
        self.level_max_time = None
        self.levels = None
        self.size = (config.levels[0].height, config.levels[0].width)

    def _display_info(self, milliseconds):
        font = pygame.font.SysFont("Arial", 18)
        screen_w = self._screen.get_width()
        screen_h = self._screen.get_height()

        # Top left: 1UP + score
        self._screen.blit(font.render("POINTS", True, (Color.WHITE)), (OFFSET_X, 8))
        self._screen.blit(font.render(str(self.score), True, (Color.WHITE)), (OFFSET_X, 28))

        # Top center: HIGH SCORE
        hs_label = font.render("HIGH SCORE", True, (Color.WHITE))
        hs_val = font.render(str(self.high_score), True, (Color.WHITE))
        cx = screen_w // 2
        self._screen.blit(hs_label, (cx - hs_label.get_width() // 2, 8))
        self._screen.blit(hs_val, (cx - hs_val.get_width() // 2, 28))

        # Top right: TIME
        elapsed = (pygame.time.get_ticks() - self._start_time) // 1000
        time_label = font.render("TIME", True, Color.WHITE)
        time_val = font.render(f"{elapsed // 60:02}:{elapsed % 60:02}", True, Color.WHITE)
        self._screen.blit(time_label, (screen_w - OFFSET_X - time_label.get_width(), 8))
        self._screen.blit(time_val, (screen_w - OFFSET_X - time_val.get_width(), 28))

        # Bottom left: life icons (lives - 1, current life not shown)
        icon_y = screen_h - OFFSET_Y // 2
        for i in range(self.lives):
            pygame.draw.circle(self._screen, (Color.YELLOW), (OFFSET_X + i * 30, icon_y), 10)

        # Cheat message: mostra per 3 secondi
        if self._cheat_time and pygame.time.get_ticks() - self._cheat_time < milliseconds:
            cheat_font = pygame.font.SysFont("Arial", 100)
            line1 = cheat_font.render("FOR THE", True, Color.YELLOW)
            line2 = cheat_font.render("FAMILY", True, Color.YELLOW)
            self._screen.blit(line1, (screen_w // 2 - line1.get_width() // 2, screen_h // 2 - line1.get_height()))
            self._screen.blit(line2, (screen_w // 2 - line2.get_width() // 2, screen_h // 2))
        else:
            self._cheat_time = None

    def _display_game_over(self, milliseconds):
        if self._game_over_time is None:
            self._game_over_time = pygame.time.get_ticks()
        elapsed = pygame.time.get_ticks() - self._game_over_time
        if elapsed >= milliseconds:
            self._game_ended = True
            self._running = False
            return
        font = pygame.font.SysFont("Arial", 60)
        game_over = font.render("GAME OVER", True, Color.RED)
        screen_w = self._screen.get_width()
        screen_h = self._screen.get_height()
        self._screen.blit(game_over, (screen_w // 2 - game_over.get_width() // 2, screen_h // 2))

    def run(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    self._key_buffer.append(event.key)
                    self._key_buffer = self._key_buffer[-max(len(CHEAT_LIVES), len(UNCHEAT)):]
                    if self._key_buffer[-len(CHEAT_LIVES):] == CHEAT_LIVES:
                        self._cheat_time = pygame.time.get_ticks()
                        self.pacman.set_cheated()
                    if self._key_buffer[-len(UNCHEAT):] == UNCHEAT:
                        self.pacman.set_normal()


            self.pacman.next_direction = pygame.key.get_pressed()
            self.pacman.update(self.maze)
            self.ghost.update(self.maze)

            hits = pygame.sprite.spritecollide(self.pacman, self.pacgums_group, True)
            for hit in hits:
                if hit.is_super:
                    self.score += self.points_per_super_pacgum
                else:
                    self.score += self.points_per_pacgum
            
            if pygame.sprite.collide_rect(self.pacman, self.ghost):
                self.lives -= 1
                if self.lives > 0:
                    self.pacman.respawn(self.maze)

            self.game_surface.fill((0, 0, 0))
            self.game_surface.blit(self.maze_surface, (0, 0))
            self.pacgums_group.draw(self.game_surface)
            self.game_surface.blit(self.pacman.image, self.pacman.rect)
            self.game_surface.blit(self.ghost.image, self.ghost.rect)
            self._screen.fill((0, 0, 0))
            self._screen.blit(self.game_surface, (OFFSET_X, OFFSET_Y))
            self._display_info(2000)
            if self.lives <= 0:
                self._display_game_over(2000)

            pygame.display.flip()
            dt = self._clock.tick(60)
        return self._game_ended


if __name__ == "__main__":
    Game().run()
    pygame.quit()
