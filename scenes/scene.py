#from game import Game


class Scene():
    def __init__(self, game):
        self.game = game
        self.prev_scene = None

    def update(self):
        pass

    def render(self, surface):
        pass

    def enter_scene(self):
        if len(self.game.scenes_stack) > 1:
            self.prev_scene = self.game.scenes_stack[-1]
        self.game.scenes_stack.append(self)

    def exit_scene(self):
        self.game.scenes_stack.pop()

    def handle_events(self, events):
        pass
