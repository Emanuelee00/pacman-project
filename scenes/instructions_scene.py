import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import pygame
from settings import Color
pygame.init()
from parser import load_highscores
from scenes.scene import Scene

class InstructionScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
    
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.exit_scene()

    def enter_scene(self):
        super().enter_scene()

    def render(self, surface):
        font = pygame.font.SysFont("Arial", 36)
        font2 = pygame.font.SysFont("Arial", 100)
        screen_w = surface.get_width()
        screen_h = surface.get_height()
        surface.fill((0, 0, 0))
        title = font.render("INSTRUCTIONS", True, Color.WHITE)
        surface.blit(title, (screen_w // 2 - title.get_width() // 2, screen_h // 4))
        text = font2.render(f"DEMERDE-TOI", True, Color.YELLOW)
        surface.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 4 + 60))
        text = font.render(f"BUT WRITE \"TORETTO\" FOR MORE", True, Color.YELLOW)
        surface.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 4 + 720))
        text = font.render(f"Use \"space\" to shoot", True, Color.YELLOW)
        surface.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 4 + 780))
        text = font.render(f"Press \"Esc\" to exit", True, Color.YELLOW)
        surface.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 4 + 840))
        