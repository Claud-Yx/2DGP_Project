from ob_tileset import *
from ob_player import *

import ob_background
import object_manager

TILE_HEIGHT = 50
TILE_WIDTH = 50


class Map:
    def __init__(self, stage, map):
        self.stage = stage
        self.map = map

        self.x, self.y = 0, 0
        self.range = [0, 0, 0, 0]

        self.size_width = 0
        self.size_height = 0

        # Game object index, 3D list
        self.object_index = [[]]

    def set_range(self):
        self.range[POS.LEFT] = self.x
        self.range[POS.BOTTOM] = self.y
        self.range[POS.RIGHT] = self.x + self.size_width
        self.range[POS.TOP] = self.y + self.size_height

    def set_size(self, w, h):
        width = w // TILE_WIDTH
        height = h // TILE_HEIGHT
        self.size_width = width * TILE_WIDTH
        self.size_height = height * TILE_HEIGHT
        self.range = [
            0, 0, self.size_width, self.size_height
        ]

        self.object_index = [[] for i in range(width)]

        for i in range(len(self.object_index)):
            self.object_index[i] = [[] for j in range(height)]

    def update(self):
        if server.time_stop:
            return
        self.clear_index()
        self.update_index()

        if self.size_width > gs_framework.canvas_width:
            if (server.player.x == gs_framework.canvas_width // 2 + 50 or
                    server.player.x == gs_framework.canvas_width // 2 - 50
            ):
                self.x -= server.player.velocity * gs_framework.frame_time

            self.x = clamp(gs_framework.canvas_width - self.size_width, self.x, 0)
        else:
            self.x = (gs_framework.canvas_width - self.size_width) / 2

    def update_index(self):
        for obj in object_manager.all_objects():
            obj: game_object.GameObject
            if (obj.__class__ == ob_background.Background or
                obj.__class__ == ob_foreground.BrickPiece or
                obj.__class__ == ob_foreground.Foreground
            ):
                continue
            if obj.bb_size_range == [-1, -1, -1, -1]:
                continue

            x1, y1, x2, y2 = obj.get_bb_size_pos()

            x1 -= self.x
            x2 -= self.x
            y1 -= self.y
            y2 -= self.y

            # if obj.type_name == TN.ENEMIES:
            #     print("%d, %d" % (obj.x - 21, x1))

            x1 //= TILE_WIDTH
            x2 //= TILE_WIDTH
            y1 //= TILE_HEIGHT
            y2 //= TILE_HEIGHT

            for x in range(int(x1), int(x2)+1):
                if x < 0 or x >= len(self.object_index):
                    continue
                for y in range(int(y1), int(y2)+1):
                    if y < 0 or y >= len(self.object_index[0]):
                        continue
                    # print("index_num: (%d, %d)" % (x, y))
                    # print("object: %s -> index" % obj.__class__.__name__)
                    try:
                        self.object_index[x][y].append(obj)
                    except:
                        print("out range pos: %s(%d, %d) / max(%d, %d)" % (obj.__class__.__name__, x, y,
                                                                           len(self.object_index),
                                                                           len(self.object_index[0])))
                        exit(-1)

    def clear_index(self):
        for x in range(len(self.object_index)):
            for y in range(len(self.object_index[x])):
                self.object_index[x][y].clear()
