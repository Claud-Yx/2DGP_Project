from abc import ABC

import object_manager
from game_object import *
from value import *

import gs_framework
import game_object

import server

MAX_JUMP_POWER = get_pps_from_mps(20)
GOOMBA_MAX_VELOCITY = get_pps_from_kmph(8)


class Enemy(game_object.GameObject, ABC):
    def __init__(self, tid=TID.NONE, x=0, y=0, x_dir=DIR.RIGHT):
        super().__init__(TN.ENEMIES, tid, x, y)

        self.x_direction = x_dir
        self.facing = x_dir

        self.jump_power = 0

        self.nearby_tiles: Set = set()

        self.timer = 0.0

    @abstractmethod
    def update(self):
        pass

    def draw(self):
        self.clip_draw()

        if self.show_bb:
            self.draw_bb()

    def handle_event(self):
        pass


class Goomba(Enemy, ABC):
    def __init__(self, x=0, y=0, x_dir=DIR.RIGHT):
        super().__init__(TID.GOOMBA, x, y, x_dir)

        self.velocity = GOOMBA_MAX_VELOCITY

        self.on_floor = False
        self.is_fall = False
        self.is_dead = False

        self.set_info(ACTION.WALK)

    def fall(self):
        self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                            ) * -1

        self.jump_power = clamp(
            MAX_JUMP_POWER * -1, self.jump_power, 0
        )

        self.y += self.jump_power * gs_framework.frame_time

    def die(self) -> bool:
        self.set_info(ACTION.DIE_A)

        if self.timer == 0:
            self.timer = 1.0

        self.timer -= gs_framework.frame_time

        if self.timer <= 0.0:
            return True
        return False

    def update(self):
        if self.is_time_stop:
            return

        server.move_camera_x(self)

        # if self.y <= -50:
        #     self.is_dead = True

        self.update_frame(gs_framework.frame_time)

        if self.is_dead:
            if self.die():
                object_manager.remove_object(self)
                del self
            return

        if not self.on_floor and not self.is_fall:
            self.is_fall = True

        if self.is_fall:
            self.on_floor = False
            self.fall()

        # print(str(self.facing), str(self.x_direction), str(self.action), str(self.velocity))
        self.x += self.velocity * gs_framework.frame_time * self.x_direction


def test_enemy():
    from ob_tileset import TileSet

    open_canvas()
    goomba = Goomba()


if __name__ == "__main__":
    test_enemy()