from parser import load_config, load_highscores
from menu_scene import MenuScene
from maze_scene import MainScene


def main():
    """Entry point of the game.

    Loads config and highscores, then runs the game loop:
    menu → game → menu → ...
    """
    config = load_config("config.json")
    highscores = load_highscores(config.highscore_filename)

    while True:
        next_scene = MenuScene.run_scene_menu()
        if next_scene:
            MainScene.run_scene_main()


if __name__ == "__main__":
    main()
