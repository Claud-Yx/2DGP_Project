from ob_map import *
from value import *

# stage_manager:
# - managing stages and maps
# - save and load maps as file
# - Stage class contains objects information each stage or map

FILE_PATH = "stage\\"
FILE_FORMAT = ".txt"
STAGE_CODE = []

current_map: Map
stage = []

# editor

class Stage:
    def __init__(self):
        self.layer = [[], [], [], [], []]
        self.map = {"stage": 0, "map": 0, "w": 0, "h": 0}
        self.player = {"tid": TID.MARIO_SMALL, "x": 0, "y": 0}
        self.enemies = []
        self.items = []
        self.tiles = []
        self.interactives = []
        self.foreground = []
        # self.background =

    def


# test ob_map.py
def test_stage_map():
    return True


if __name__ == "__main__":
    print("== ob_map.py is prepared.")
    print("== start testing ob_map.py\n")
    if test_stage_map():
        print("\n== testing ob_map.py is done.")
    else:
        print("\n== error: testing ob_map.py is crashed")
