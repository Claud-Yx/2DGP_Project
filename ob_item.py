from abc import ABC

import object_manager
import server
from game_object import *
from value import *

import game_object
import gs_framework

MAX_JUMP_POWER = get_pps_from_mps(15)
MAX_VELOCITY = get_pps_from_kmph(10)


class Item(game_object.Object, ABC):
    def __init__(self, tid=TID.NONE, x=0, y=0, x_dir=DIR.RIGHT):
        super().__init__(TN.ITEMS, tid, x, y)

        self.x_direction = x_dir

        self.jump_power = 0

        self.nearby_tiles: Set = set()

        self.is_dead = False

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
    def __init__(self, x=0, y=0, x_dir=DIR.RIGHT):
        super(). __init__(TID.SUPER_MUSHROOM, x, y, x_dir)

        self.velocity = MAX_VELOCITY

        self.on_floor = False
        self.is_fall = False

        self.set_info(ACTION.WALK)

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

        if self.is_dead:
            object_manager.remove_object(self)
            del self
            return

        if not self.on_floor and not self.is_fall:
            self.is_fall = True

        if self.is_fall:
            self.on_floor = False
            self.fall()

        self.x += self.velocity * gs_framework.frame_time * self.x_direction
        pass















