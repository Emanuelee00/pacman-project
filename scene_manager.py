from menu_scene import MenuScene
from game_scene import Game
from name_input_scene import NameInputScene
import sys
import pygame
import parser

pygame.init()

print(sys.argv[0])
argc = len(sys.argv[:])

if argc == 2:
    try:
        config = parser.load_config(sys.argv[1])
        game = Game(config)
    except (ValueError) as e:
        print(e)
    except (FileNotFoundError) as e:
        print(str(e)[10:])
else:
    game = Game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    next_scene = MenuScene.run_scene_menu()
    if next_scene:
        game_ended = game.run()
        if game_ended:
            NameInputScene(game._screen, game.score).run()

pygame.quit()
