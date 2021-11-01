from pico2d import *
from value import *
from tileset_object import *
from player import *

from enemy_goomba import *
from enemy_drybones import *

class StageMap:
    def __init__(self):
        self.world = 0
        self.stage = 0
        self.map = 0

        self.size = [0, 0]
        self.player = None

        self.object = [[] for i in range(OT.SIZE)]

        self.file_path = "stage\\"
        self.file_format = ".txt"
        self.stage_code = []

    def set_size(self, size=[]):
        self.size = [size[0] * 50, size[1] * 50]

    def set_object(self, player, tilesets=[], enemies=[], items=[], interactives=[]):
        self.player = player
        self.object[OT.TILESETS] = tilesets
        self.object[OT.ENEMIES] = enemies
        self.object[OT.ITMES] = items
        self.object[OT.INTERACTIVES] = interactives

    def read_stage_file(self, file_name):
        file = open(self.file_path + file_name + self.file_format, 'r')
        while True:
            line = file.readline()
            if not line:
                break
            self.stage_code.insert(0, line)
        file.close()

    def decode_stage_file(self):

        # stage information
        file_info = self.stage_code.pop()

        if not file_info[0:4] == "INFO":
            return False

        if not file_info[4] == "n":
            return False

        self.world = int(file_info[5]) * 10 + int(file_info[6])
        self.stage = int(file_info[7]) * 10 + int(file_info[8])
        self.map = int(file_info[9]) * 10 + int(file_info[10])

        if not file_info[11] == "w" and not file_info[14] == "h":
            return False

        self.set_size(
            [int(file_info[12]) * 10 + int(file_info[13]),
             int(file_info[15]) * 10 + int(file_info[16])]
        )

        # map data
        # from bottom line
        while 0 < len(self.stage_code):
            line = self.stage_code.pop(0)
            x, y = 0, 0
            index = 0

            while index < len(line):
                is_size = True
                if '.' == line[index]:
                    x += (int(line[index + 1]) * 100 +
                          int(line[index + 2]) * 10 +
                          int(line[index + 3]))
                    index += 4
                    is_size = False

                elif 'p' == line[index]:
                    pass

                elif 'e' == line[index]:
                    id = (int(line[index + 1]) * 10 +
                          int(line[index + 2]))
                    index += 3

                    if TID.GOOMBA == id:
                        pass

                    elif TID.DRY_BONES == id:
                        pass

                    elif TID.BOO == id:
                        pass

                    elif TID.PIRANHA_PLANT == id:
                        pass

                    elif TID.SPIKE_BALL == id:
                        pass

                    elif TID.BOSS == id:
                        pass

                    else:
                        print("ERROR: Undefined Enemy Type ID")
                        return False

                elif 'd' == line[index]:
                    pass

                elif 'P' == line[index]:
                    pass

                elif 't' == line[index]:
                    pass

                elif 'i' == line[index]:
                    pass

                elif 'a' == line[index]:
                    pass


        return True




def test_stage_map():
    stage = StageMap()
    stage.read_stage_file('000000.txt')
    print(stage.stage_code)

    stage.decode_stage_file()
    print(stage.world)
    print(stage.stage)
    print(stage.map)
    print(stage.size)

    return True


if __name__ == "__main__":
    print("== stage_map.py is prepared.")
    print("== start testing stage_map.py\n")
    if test_stage_map():
        print("\n== testing stage_map.py is done.")
    else:
        print("\n== error: testing stage_map.py is crashed")
