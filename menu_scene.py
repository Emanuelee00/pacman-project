import pygame
from pygame import event
# from game import Game
from play_scene import PlayScene
from scene import Scene
from settings import (
     SCREEN_WIDTH,
     SCREEN_HEIGHT,
)
from parser import GameConfig, load_highscores


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.mid_w, self.mid_h = self.game.screen.get_width() // 2, self.game.screen.get_height() // 2
        print(self.game.screen.get_width())
        print(self.game.screen.get_height())

        self.options = {
            0: {
                'name': "PLAY",
                'position': (self.mid_w, self.mid_h - 60),
            },
            1: {
                'name': "INSTRUCTIONS",
                'position': (self.mid_w, self.mid_h),
            },
            2: {
                'name': "HIGH SCORES",
                'position': (self.mid_w, self.mid_h + 60),
            },
            3: {
                'name': "EXIT",
                'position': (self.mid_w, self.mid_h + 120),
            }
        }
        self.selected_option = 0

        self.cursor_img = pygame.image.load("assets/arrow.png").convert_alpha()
        self.cursor_img = pygame.transform.scale(self.cursor_img, (18, 18))
        self.cursor_rect = self.cursor_img.get_rect()

    def handle_events(self, events: list[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.selected_option = (
                        (self.selected_option + 1) % len(self.options)
                        )
                if e.key == pygame.K_UP:
                    self.selected_option = (
                        (self.selected_option - 1) % len(self.options)
                        )
                if e.key == pygame.K_RETURN:
                    self._select_option()

    def _select_option(self):
        match self.selected_option:
            case 0:
                PlayScene(self.game).enter_scene()
                pass
            case 1:
                # HighScoresScene(self.game).enter_state()
                pass
            case 2:
                # InstructionsScene(self.game).enter_state()
                pass
            case 3:
                self.game.running = False

    def render(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(self.cursor_img, self.cursor_rect)
        for idx, option in self.options.items():
            color = (255, 255, 0) if idx == self.selected_option else (255, 255, 255)
            text_rect = self.game.draw_text(surface, option['name'], color, *option['position'])
            if idx == self.selected_option:
                self.cursor_rect.center = (
                    option['position'][0] - text_rect.width // 2 - 20,
                    option['position'][1]
                )


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
        levels=[]
    )
    game = Game()
    menu_scene = MenuScene(game)
    game.run()
