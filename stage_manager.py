from ob_map import *
from value import *

# stage_manager:
# - managing stages and maps
# - save and load maps as file
# - Stage class contains objects information each stage or map

FILE_PATH = "stage\\"
FILE_FORMAT = ".stg"

current_map: Map
stage = {}

# editor

class Stage:
    stage_num = 1
    map_num = 1

    def __init__(self, file_name):
        self.objects = None
        self.map = None

        self.load_stage(file_name)

    def load_stage(self, file_name):
        import pickle
        with open(file_name, 'rb') as f:
            data = pickle.load(f)
            self.map = data.pop()
            self.objects = data


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
