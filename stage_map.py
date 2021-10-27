from pico2d import *
from value import *
from tileset_object import *
from player import *

from enemy_goomba import *
from enemy_drybones import *

class StageMap:
    def __init__(self):
        self.size = [0, 0]
        self.player = None

        self.object = [[] for i in range(OT.SIZE)]

        self.file_path = "stage\\"
        self.stage_code = []

    def set_size(self, size=[]):
        self.size = [size[0] * 50, size[1] * 50]

    def set_player_pos(self, pos=[]):
        self.player_pos = pos

    def set_object(self, player, tilesets=[], enemies=[], items=[], interactives=[]):
        self.player = player
        self.object[OT.TILESETS] = tilesets
        self.object[OT.ENEMIES] = enemies
        self.object[OT.ITMES] = items
        self.object[OT.INTERACTIVES] = interactives

    def get_stage_file(self, file_name):
        file = open(self.file_path + file_name, 'r')
        while True:
            line = file.readline()
            if not line:
                break
            self.stage_code.insert(0, line)
