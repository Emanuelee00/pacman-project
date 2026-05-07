CELL_SIZE = 40
WS = 10
TS = CELL_SIZE + WS * 2
TS_D1 = TS + 1
TS_D2 = TS + 3

class SettingManager():
    screen_size = (TS * 18, TS * 18)
    
    @staticmethod
    def get_screen_size():
        return SettingManager.screen_size


