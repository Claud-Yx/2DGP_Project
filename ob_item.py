import object_manager
from game_object import *
from value import *

import game_object
import gs_framework

class Item(game_object.Object):
    def __init__(self, tid=TID.NONE, x=0, y=0, x_dir=DIR.RIGHT):
        super().__init__(TN.ITEMS, tid, x, y)

        