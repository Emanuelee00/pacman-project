from menu_scene import MenuScene
from pacman_movements import MainScene

while True:
    next_scene = MenuScene.run_scene_menu()
    if next_scene:
        MainScene.run_scene_main()

