from pico2d import *
from value import *
from ob_tileset import *
from ob_player import *

TILE_HEIGHT = 50
TILE_WIDTH = 50

class Map:
    def __init__(self):
        self.stage = 0
        self.map = 0

        self.size_width = 0
        self.size_height = 0
        self.player = None

        # Game object index, 3D list
        self.object_index = []

    def set_size(self, w, h):
        self.size_width = w // TILE_WIDTH * TILE_WIDTH
        self.size_height = h // TILE_HEIGHT * TILE_HEIGHT


