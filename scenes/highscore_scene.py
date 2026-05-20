import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import pygame
from settings import Color
pygame.init()
from parser import load_highscores
from scenes.scene import Scene

class highScoreScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.top_5: dict = {}

    def _top_5(self):
        highscores = load_highscores(str(Path(__file__).parent.parent / "highscores.json"))
        top5 = sorted(highscores.scores, key=lambda score: score.score, reverse=True)
        for value in top5:
            self.top_5[value.name] = value.score
        print(top5)
        return top5
    
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.exit_scene()

    def enter_scene(self):
        self._top_5()
        super().enter_scene()

    def render(self, surface):
        font = pygame.font.SysFont("Arial", 36)
        screen_w = surface.get_width()
        screen_h = surface.get_height()
        surface.fill((0, 0, 0))
        title = font.render("HIGH SCORES", True, Color.WHITE)
        surface.blit(title, (screen_w // 2 - title.get_width() // 2, screen_h // 4))
        for i, (name, score) in enumerate(self.top_5.items()):
            if i < 5:
                text = font.render(f"{i + 1}. {name}  {score}", True, Color.YELLOW)
                surface.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 4 + 60 + i * 50))

