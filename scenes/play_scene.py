import pygame
from characters.ghosts import Blinky, Clyde, Inky, Pinky
from characters.pacman import Pacman
from settings import (
    WALL_SIZE,
    CELL_SIZE,
    OFFSET_X,
    OFFSET_Y,
    CHEAT_LIVES,
    UNCHEAT,
    Color
)
from mazegenerator.mazegenerator import MazeGenerator
from maze_drawing import draw_maze, to_tile_map
from pacgum import PacgumManager
from .scene import Scene
from .name_input_scene import NameInputScene

class PlayScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.size = (
            self.game.levels[self.game.current_level].height,
            self.game.levels[self.game.current_level].width
            )
        maze_h, maze_w = self.size
        tilemap_w = WALL_SIZE + CELL_SIZE * maze_w
        tilemap_h = WALL_SIZE + CELL_SIZE * maze_h
        self.game_canvas = pygame.Surface((
            tilemap_w,
            tilemap_h + 2 * OFFSET_Y,
            )
            )

        self.maze_gen = MazeGenerator(size=self.size, seed=self.game.seed)
        self.maze = self.maze_gen.maze
        self.tilemap = to_tile_map(self.maze)

        self.maze_surface = pygame.Surface((tilemap_w, tilemap_h))
        draw_maze(
            self.maze_surface,
            self.tilemap,
            self.maze,
            self.game.assets["maze_tiles"])

        self._load_characters()
        self._key_buffer = []
        self.missiles = pygame.sprite.Group()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._key_buffer.append(event.key)
                self._key_buffer = self._key_buffer[-max(len(CHEAT_LIVES), len(UNCHEAT)):]
                if self._key_buffer[-len(CHEAT_LIVES):] == CHEAT_LIVES:
                    self._cheat_time = pygame.time.get_ticks()
                    self.pacman.set_cheated()
                if self._key_buffer[-len(UNCHEAT):] == UNCHEAT:
                    self.pacman.set_normal()
                if event.key == pygame.K_SPACE:
                    self.pacman.shoot(self.missiles)

    def _load_characters(self):
        self.pacman = Pacman(
            maze=self.maze,
            spritesheet=self.game.assets["pacman_sprites"],
        )
        self.pacgums = PacgumManager(self.maze).group
        self.ghosts = pygame.sprite.Group()
        self.ghosts.add(
            Blinky(
                maze=self.maze,
                pacman=self.pacman,
                spritesheet=self.game.assets["ghosts_sprites"]
                ),
            Pinky(
                maze=self.maze,
                pacman=self.pacman,
                spritesheet=self.game.assets["ghosts_sprites"]),
            Clyde(
                self.maze,
                self.pacman,
                self.game.assets["ghosts_sprites"])
            )
        self.ghosts.add(
            Inky(
                maze=self.maze,
                pacman=self.pacman,
                blinky=self.ghosts.sprites()[0],
                spritesheet=self.game.assets["ghosts_sprites"]
                )
            )

        self.pacman.respawn()
        for ghost in self.ghosts:
            ghost.respawn()

    def _check_collisions(self, group):
        return pygame.sprite.spritecollide(self.pacman, group, True)

    def update(self) -> None:
        self.pacman.next_direction = pygame.key.get_pressed()
        self.pacman.update()
        self.ghosts.update()
        self.pacgums.update()
        self.missiles.update()

        hits = self._check_collisions(self.pacgums)
        for hit in hits:
            if hit.is_super:
                self.game.score += self.game.points_per_super_pacgum
            else:
                self.game.score += self.game.points_per_pacgum

        for ghost in self.ghosts:
            if ghost.rect.collidepoint(self.pacman.rect.centerx, self.pacman.rect.centery):
                self.game.lives -= 1
                if self.game.lives > 0:
                    self.pacman.respawn()

        for missile in list(self.missiles):
            hit_ghosts = pygame.sprite.spritecollide(missile, self.ghosts, True)
            if hit_ghosts:
                self.game.score += 200 * len(hit_ghosts)
                missile.kill()
            for hit in pygame.sprite.spritecollide(missile, self.pacgums, True):
                if hit.is_super:
                    self.game.score += self.game.points_per_super_pacgum
                else:
                    self.game.score += self.game.points_per_pacgum

        if len(self.pacgums) == 0:
            NameInputScene(self.game.screen, self.game.score).run()
            self.exit_scene()

    def _display_info(self):
        font = pygame.font.Font(self.game.current_dir / "assets" / "Pixel_Digivolve.otf", 18)

        # Top left: 1UP + score
        self.game_canvas.blit(font.render("POINTS", True, (255, 255, 0)), (0, 0))
        self.game_canvas.blit(font.render(str(self.game.score), True, (Color.WHITE)), (0, 20))

        # Top center: HIGH SCORE
        hs_label = font.render("HIGH SCORE", True, (255, 255, 0))
        hs_val = font.render(str(self.game.high_score), True, (Color.WHITE))
        cx = self.game_canvas.get_width() // 2
        self.game_canvas.blit(hs_label, (cx - hs_label.get_width() // 2, 0))
        self.game_canvas.blit(hs_val, (cx - hs_val.get_width() // 2, 20))

        # Top right: TIME
        elapsed = (pygame.time.get_ticks() - self.game._start_time) // 1000
        time_label = font.render("TIME", True, (255, 255, 0))
        time_val = font.render(f"{elapsed // 60:02}:{elapsed % 60:02}", True, (Color.WHITE))
        self.game_canvas.blit(time_label, (self.game_canvas.get_width() - time_label.get_width(), 0))
        self.game_canvas.blit(time_val, (self.game_canvas.get_width() - time_val.get_width(), 20))

        # Bottom left: life icons (lives - 1, current life not shown)
        icon_y = self.game_canvas.get_height() - OFFSET_Y // 2
        for i in range(self.game.lives):
            pygame.draw.circle(self.game_canvas, (Color.YELLOW), (OFFSET_X + i * 30, icon_y), 10)

        # Cheat message: mostra per 3 secondi
        # if self._cheat_time and pygame.time.get_ticks() - self._cheat_time < milliseconds:
        #     cheat_font = pygame.font.SysFont("Arial", 100)
        #     line1 = cheat_font.render("FOR THE", True, Color.YELLOW)
        #     line2 = cheat_font.render("FAMILY", True, Color.YELLOW)
        #     self.game_canvas.blit(line1, (self.game_canvas.get_width() // 2 - line1.get_width() // 2, self.game_canvas.get_height() // 2 - line1.get_height()))
        #     self.game_canvas.blit(line2, (self.game_canvas.get_width() // 2 - line2.get_width() // 2, self.game_canvas.get_height() // 2))
        # else:
        #     self._cheat_time = None

    def render(self, surface):
        # prepare canvas: clear, draw static maze, then sprites + HUD
        self.game_canvas.fill((0, 0, 0))
        self.game_canvas.blit(self.maze_surface, (0, OFFSET_Y))

        for pacgum in self.pacgums:
            self.game_canvas.blit(
                pacgum.image,
                (pacgum.rect.x, pacgum.rect.y + OFFSET_Y),
            )

        for ghost in self.ghosts:
            self.game_canvas.blit(
                ghost.image,
                (ghost.rect.x, ghost.rect.y + OFFSET_Y),
            )

        self.game_canvas.blit(
            self.pacman.image,
            (self.pacman.rect.x, self.pacman.rect.y + OFFSET_Y),
        )

        for missile in self.missiles:
            self.game_canvas.blit(
                missile.image,
                (missile.rect.x, missile.rect.y + OFFSET_Y)
            )

        self._display_info()

        surface.blit(
            self.game_canvas,
            (
                surface.get_width() // 2 - self.game_canvas.get_width() // 2,
                surface.get_height() // 2 - self.game_canvas.get_height() // 2,
            )
        )
