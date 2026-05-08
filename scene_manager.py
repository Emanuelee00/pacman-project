from menu_scene import MenuScene
from maze_scene import MainScene

while True:
    next_scene = MenuScene.run_scene_menu()
    if next_scene:
        MainScene.run_scene_main()

