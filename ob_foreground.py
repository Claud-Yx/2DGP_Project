import random

from pico2d import *
import game_object
import gs_framework

from value import *

BRICK_PIECE_RAD = 360


class Foreground(game_object.GameObject):
    def __init__(self, x, y, ptn=TN.NONE, ptid=TID.NONE):
        super().__init__(TN.FOREGROUND, TID.NONE, x, y)

        del self.bounding_box
        del self.bb_size_range
        del self.show_bb

        self.rad = 0
        self.pm_type_name = ptn
        self.pm_type_id = ptid

        self.is_animated = False

    def update(self):
        pass

    def draw(self):
        if self.is_animated:
            self.update_frame(gs_framework.frame_time)
            self.clip_draw(self.pm_type_id, self.pm_type_id, self.rad)

        else:
            self.image_draw(self.pm_type_name, self.pm_type_id, self.rad)

    def handle_event(self, event):
        pass


class BrickPiece(Foreground):
    def __init__(self, x, y, piece):
        super().__init__(x, y, TN.FOREGROUND, TID.BRICK_PIECE)

        self.action = piece
        self.set_clip()

    def update(self):
        pass

    def draw(self):
        self.update_frame(gs_framework.frame_time)
        self.clip_draw(self.pm_type_id, self.pm_type_id, self.rad)
