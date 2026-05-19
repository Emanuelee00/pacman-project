import pygame
from game import Game
from scene import Scene
from settings import (
     SCREEN_WIDTH,
     SCREEN_HEIGHT,
     FPS
)

class MenuScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.mid_w, self.mid_h = self.game.screen.get_width() // 2, self.game.screen.get_height() // 2
        self.offset = - 50
        self.options = ["PLAY", "HIGHSCORES", "INSTRUCTIONS", "EXIT"]
        self.selected_option = 0

        self.options_pos = {
            0: (self.mid_w, self.mid_h - 60),
            1: (self.mid_w, self.mid_h),
            2: (self.mid_w, self.mid_h + 60),
            3: (self.mid_w, self.mid_h + 120)
        }

        self.cursor_img = pygame.image.load("assets/cursor.png").convert_alpha()
        self.cursor_img = pygame.transform.scale(self.cursor_img, (32, 32))
        self.cursor_rect = self.cursor_img.get_rect()

    def handle_events(self, events):
        for event in events:
            if event.key == pygame.K_DOWN:
                self.selected_option = (
                    (self.selected_option + 1) % len(self.options)
                    )
            if event.key == pygame.K_UP:
                self.selected_option = (
                    (self.selected_option - 1) % len(self.options)
                    )
            if event.key == pygame.K_KP_ENTER:
                self.update()

    def update(self):
        match self.selected_option:
            case 0:
                # PlayScene(self.game).enter_state()
                pass
            case 1:
                # HighScoresScene(self.game).enter_state()
                pass
            case 2:
                # InstructionsScene(self.game).enter_state()
                pass
            case 3:
                pygame.quit()
                exit()

    def render(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(self.cursor_img, self.cursor_rect)
        surface.game.draw_text(
            surface,
            self.options[0],
            (255, 255, 255),

            )

    # @staticmethod
    # def run_scene_menu():
    #     pygame.init()
    #     screen = pygame.display.set_mode(SCREEN_SIZE)
    #     clock = pygame.time.Clock()
    #     running = True
    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False
    #             if event.type == pygame.KEYDOWN:
    #                 if event.key in (
    #                     pygame.K_RETURN,
    #                     pygame.K_KP_ENTER):
    #                     return True

    #         screen.fill("black")

    #         title_font = pygame.font.SysFont("Arial", 70)
    #         message_font = pygame.font.SysFont("Arial", 40)
    #         title_surface = title_font.render("PACMAN", True, "Yellow")
    #         message_surface = message_font.render("Press ENTER to play", True, "White")
    #         screen.blit(title_surface, (300, 100))
    #         screen.blit(message_surface, (300, 300))




    #                 # print(f"x={x}, y={y}, TS={TS}")
    #                 # print(f"res={curr_pos & 1}")


    #         pygame.display.flip()
    #         dt = clock.tick(60)

    #     pygame.quit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu_scene = MenuScene(Game())
    menu_scene.enter_scene()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_scene = menu_scene.game.scenes_stack[-1]
        current_scene.handle_events(pygame.event.get())
        current_scene.render(screen)
        pygame.display.flip()

    pygame.quit()
