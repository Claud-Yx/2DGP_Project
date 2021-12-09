from pico2d import *

import gs_framework
import ob_background
import object_manager
import server
from value import *

TILE_HEIGHT = 50
TILE_WIDTH = 50


class Map:
    def __init__(self, stage, map, w, h, timer=200):
        self.stage = stage
        self.map = map

        self.x, self.y = 0, 0
        self.range = [0, 0, 0, 0]

        self.size_width = 0
        self.size_height = 0

        self.timer_stage = timer

        # Game object index, 3D list
        self.object_index = [[]]

        self.set_size(w, h)

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

        if self.size_width <= gs_framework.canvas_width:
            self.x = (gs_framework.canvas_width - self.size_width) / 2
        if self.size_height <= gs_framework.canvas_height:
            self.y = (gs_framework.canvas_height - self.size_height) / 2

    def update_index(self):
        import game_object
        import ob_foreground

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

            # x1 -= self.x
            # x2 -= self.x
            # y1 -= self.y
            # y2 -= self.y

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

    def move(self):
        if self.size_width > gs_framework.canvas_width:
            self.x = -(server.player.ax - server.player.rx)
            self.x = clamp(gs_framework.canvas_width - self.size_width, self.x, 0)

        if self.size_height > gs_framework.canvas_height:
            self.y = -(server.player.ay - server.player.ry)
            self.y = clamp(gs_framework.canvas_height - self.size_height, self.y, 0)

    def print_index(self):
        for y in range(len(self.object_index[0])):
            for x in range(len(self.object_index)):
                print("[%d][%d]: %s" % (x, y, self.object_index[x][y]))

    def clear_index(self):
        for x in range(len(self.object_index)):
            for y in range(len(self.object_index[x])):
                self.object_index[x][y].clear()

    def update(self):
        if server.time_stop:
            return

        self.timer_stage -= gs_framework.frame_time
        if self.timer_stage <= 0:
            server.player.is_small = True
            server.player.type_id = TID.MARIO_SMALL
            server.player.is_damaged = True

        self.clear_index()
        self.update_index()

        self.move()
