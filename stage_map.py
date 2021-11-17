from pico2d import *
from value import *
from tileset import *
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

        self.object = [list() for i in range(TN.SIZE)]

        self.file_path = "stage\\"
        self.file_format = ".txt"
        self.stage_code = []

    def set_size(self, size=[]):
        self.size = [size[0] * 50, size[1] * 50]

    def set_object(self, player, tilesets=[], enemies=[], items=[], interactives=[], foregrounds=[]):
        self.player = player
        self.object[TN.TILESETS] = tilesets
        self.object[TN.ENEMIES] = enemies
        self.object[TN.ITMES] = items
        self.object[TN.INTERACTIVES] = interactives
        self.object[TN.FOREGROUND] = foregrounds

    def read_stage_file(self, file_name):
        file = open(self.file_path + file_name + self.file_format, 'r')
        while True:
            line = file.readline()
            if not line:
                break
            self.stage_code.insert(0, line)
        file.close()

    def create_object(self, tname, tid, lx, ly, count=1, foreground=False):
        pass


    def decode_stage_file(self):

        # stage information
        file_info = self.stage_code.pop()

        if not file_info[0:4] == "INFO":
            print("ERROR: Undefined INFO line")
            return False

        if not file_info[4] == "n":
            print("ERROR: Undefined INFO name code")
            return False

        self.world = int(file_info[5]) * 10 + int(file_info[6])
        self.stage = int(file_info[7]) * 10 + int(file_info[8])
        self.map = int(file_info[9]) * 10 + int(file_info[10])

        if not file_info[11] == "w" and not file_info[14] == "h":
            print("ERROR: Undefined INFO w/h code")
            return False

        self.set_size(
            [int(file_info[12]) * 10 + int(file_info[13]),
             int(file_info[15]) * 10 + int(file_info[16])]
        )

        # map data
        player = None
        tilesets = []
        enemies = []
        items = []
        interactives = []
        foregrounds = []

        lx, ly = 0, 0  # file line position(left bottom) / 1 = 50px
        object_lx = 0  # object file line position(left bottom) / 1 = 50px
        index = 0  # file line cursor
        type_name, type_id = 0, 0  # type_name: player, enemy... / type_id: mario, goomba...

        # y axis
        # from bottom line
        while 0 < len(self.stage_code):
            line = self.stage_code.pop(0)
            index = 0
            lx = 0

            # x axis
            while index < len(line):
                is_foreground = False
                object_lx = 0
                type_name, type_id = 0, 0
                count = 1

                # foreground
                if 'f' == line[index]:
                    is_foreground = True

                # blank
                if '.' == line[index]:
                    lx += (int(line[index + 1]) * 100 +
                           int(line[index + 2]) * 10 +
                           int(line[index + 3]))
                    index += 4

                # if not blank
                else:
                    type_name = line[index]
                    index += 1

                    # player
                    if 'p' == type_name:
                        type_id = 0

                    # enemies
                    elif 'e' == type_name:
                        type_id = (int(line[index]) * 10 +
                                   int(line[index + 1]))
                        index += 2

                    # door
                    elif 'd' == type_name:
                        pass

                    # pipe
                    elif 'P' == type_name:
                        pass

                    # tilesets
                    elif 't' == type_name:
                        type_id = (int(line[index]) * 10 +
                                   int(line[index + 1]))
                        index += 2

                    # items
                    elif 'i' == type_name:
                        pass

                    # interactive things
                    elif 'a' == type_name:
                        pass

                    else:
                        print("ERROR: Undefined TypeName")
                        return False

                    # size
                    if 'w' == line[index]:
                        object_lx = lx

                        lx += (int(line[index + 1]) * 100 +
                                 int(line[index + 2]) * 10 +
                                 int(line[index + 3]))
                        index += 4

                    else:
                        print("ERROR: Undefined width code")
                        return False

                    # useless?
                    # if 'h' == line[index]:
                    #     ly += (int(line[index + 1]) * 100 +
                    #            int(line[index + 2]) * 10 +
                    #            int(line[index + 3]))
                    #     index += 4
                    # else:
                    #     print("ERROR: Undefined height code")
                    #     return False

                    if 'C' == line[index]:
                        count = (int(line[index + 1]) * 100 +
                                 int(line[index + 2]) * 10 +
                                 int(line[index + 3]))
                        index += 4

                self.create_object(type_name, type_id, object_lx, ly, count, is_foreground)
            ly += 1

        return True


# test stage_map.py
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
