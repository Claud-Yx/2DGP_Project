from abc import ABC

import object_manager
import server
from game_object import *
from value import *

import gs_framework

MAX_JUMP_POWER = get_pps_from_mps(15)
MAX_VELOCITY = get_pps_from_kmph(10)

COIN_POPUP_VELOCITY = 1000
COIN_POPUP_DISTANCE = 150
COIN_POPUP_ACCEL = 3000

ITEM_POPUP_DISTANCE = 50
ITEM_POPUP_VELOCITY = 50


class Item(GameObject, ABC):
    def __init__(self, tid=TID.NONE, x=0, y=0, x_dir=DIR.RIGHT):
        super().__init__(TN.ITEMS, tid, x, y)

        self.pop_y_max = 0
        self.x_direction = x_dir

        self.jump_power = 0

        self.nearby_tiles: Set = set()

        self.is_dead = False
        self.in_box = False

    @abstractmethod
    def update(self):
        pass

    def draw(self):
        self.image_draw()

        if self.show_bb:
            self.draw_bb()

    def handle_event(self):
        pass


class SuperMushroom(Item, ABC):
    def __init__(self, x=0, y=0, x_dir=DIR.RIGHT, in_box=False):
        super(). __init__(TID.SUPER_MUSHROOM, x, y, x_dir)

        self.velocity = MAX_VELOCITY

        self.on_floor = False
        self.is_fall = False
        self.in_box = in_box

        self.set_info(ACTION.WALK)

        if self.in_box:
            self.switch_bb_all()

    def fall(self):
        self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                            ) * -1

        self.jump_power = clamp(
            MAX_JUMP_POWER * -1, self.jump_power, 0
        )

        self.y += self.jump_power * gs_framework.frame_time

    def update(self):
        if self.is_time_stop:
            return

        server.move_camera_x(self)

        if self.in_box:
            if self.pop_y_max == 0:
                self.pop_y_max = self.y + ITEM_POPUP_DISTANCE
            self.y += ITEM_POPUP_VELOCITY * gs_framework.frame_time
            if self.y >= self.pop_y_max:
                self.y = self.pop_y_max + 1
                self.in_box = False
                self.switch_bb_all(True)
            return

        if self.is_dead:
            object_manager.remove_object(self)
            del self
            return

        if not self.on_floor and not self.is_fall and not self.in_box:
            self.is_fall = True

        if self.is_fall and not self.in_box:
            self.on_floor = False
            self.fall()

        self.x += self.velocity * gs_framework.frame_time * self.x_direction
        pass


class Coin(Item, ABC):
    def __init__(self, x=0, y=0, in_box=False):
        super().__init__(TID.COIN, x, y)

        self.is_dead = False
        self.in_box = in_box
        self.pop_y_max = 0
        self.pop_y_min = 0
        self.y_acceleration = 0

        self.set_size(0.8, 0.8)


        # print("in box coin, pos: (%.2f, %.2f) / in_box: %s" % (self.x, self.y, self.in_box))

    def update(self):
        if self.is_time_stop:
            return

        server.move_camera_x(self)

        if self.in_box:
            if self.pop_y_max == 0:  # init
                self.switch_bb_all()
                self.set_size(0.6, 0.8)
                self.pop_y_max = self.y + COIN_POPUP_DISTANCE
                self.pop_y_min = self.pop_y_max - COIN_POPUP_DISTANCE // 2
                self.set_tpa(0.2)

            self.y += (COIN_POPUP_VELOCITY - self.y_acceleration) * gs_framework.frame_time
            self.y_acceleration += COIN_POPUP_ACCEL * gs_framework.frame_time

            if self.y_acceleration > COIN_POPUP_ACCEL * (3/5):
                self.is_dead = True

        self.update_frame(gs_framework.frame_time)

        if self.is_dead:
            object_manager.remove_object(self)
            del self
            return

    def draw(self):
        self.clip_draw()

        if self.show_bb:
            self.draw_bb()















