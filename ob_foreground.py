from pico2d import *
import game_object
import gs_framework

from value import *


class Foreground(game_object.GameObject):
    def __init__(self, x, y, ptn=TN.NONE, ptid=TID.NONE):
        super().__init__(TN.FOREGROUND, TID.NONE, x, y)

        del self.bounding_box
        del self.bb_size_range
        del self.show_bb

        self.pm_type_name = ptn
        self.pm_type_id = ptid

    def update(self):
        pass

    def draw(self, animate=False, rad=0):
        if animate:
            self.update_frame(gs_framework.frame_time)
            self.clip_draw(self.pm_type_id, self.pm_type_id, rad)

        else:
            self.image_draw(self.pm_type_name, self.pm_type_id, rad)

    def handle_event(self, event):
        pass
