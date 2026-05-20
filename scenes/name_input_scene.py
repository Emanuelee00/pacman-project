import pygame
from settings import Color
from parser import load_highscores, HighscoreEntry, save_highscores


class NameInputScene:
    def __init__(self, screen: pygame.Surface, score: int) -> None:
        self._screen = screen
        self._score = score
        self._player_name = ""
        self._error_msg = ""

    def _draw(self):
        font = pygame.font.SysFont("Arial", 36)
        screen_w = self._screen.get_width()
        screen_h = self._screen.get_height()
        self._screen.fill((0, 0, 0))
        prompt = font.render("INSERT NAME:", True, Color.WHITE)
        name = font.render(self._player_name + "_", True, Color.YELLOW)
        self._screen.blit(prompt, (screen_w // 2 - prompt.get_width() // 2, screen_h // 2 - 50))
        self._screen.blit(name, (screen_w // 2 - name.get_width() // 2, screen_h // 2 + 10))
        if self._error_msg:
            err_font = pygame.font.SysFont("Arial", 22)
            err = err_font.render(self._error_msg, True, Color.RED)
            self._screen.blit(err, (screen_w // 2 - err.get_width() // 2, screen_h // 2 + 60))

    def run(self) -> str:
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self._player_name
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if len(self._player_name) < 3:
                            self._error_msg = "Name must be at least 3 characters"
                        else:
                            hs = load_highscores()
                            hs.scores.append(HighscoreEntry(name=self._player_name, score=self._score))
                            save_highscores(hs)
                            return self._player_name
                    elif event.key == pygame.K_BACKSPACE:
                        self._player_name = self._player_name[:-1]
                        self._error_msg = ""
                    elif event.unicode.isprintable():
                        if len(self._player_name) < 20:
                            self._player_name += event.unicode
                            self._error_msg = ""
                        else:
                            self._error_msg = "Name must be less than 20 characters"

            self._draw()
            pygame.display.flip()
            clock.tick(60)
