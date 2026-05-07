import pygame
from setting_manager import SettingManager


dt = 0

class MenuScene():
    @staticmethod
    def run_scene_menu():
        pygame.init()
        screen = pygame.display.set_mode(SettingManager.get_screen_size())
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in (
                        pygame.K_RETURN, 
                        pygame.K_KP_ENTER):
                        return True

            screen.fill("black")

            title_font = pygame.font.SysFont("Arial", 70)
            message_font = pygame.font.SysFont("Arial", 40)
            title_surface = title_font.render("PACMAN", True, "Yellow")
            message_surface = message_font.render("Press ENTER to play", True, "White")
            screen.blit(title_surface, (300, 100))
            screen.blit(message_surface, (300, 300))




                    # print(f"x={x}, y={y}, TS={TS}")
                    # print(f"res={curr_pos & 1}")


            pygame.display.flip()
            dt = clock.tick(60)

        pygame.quit()