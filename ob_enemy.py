from game_object import *
from value import *

import gs_framework
import game_object

MAX_JUMP_POWER = get_pps_from_mps(20)


class Enemy(game_object.Object):
    def __init__(self, tid=TID.NONE, x=0, y=0, x_dir=DIR.RIGHT):
        super().__init__(TN.ENEMIES, tid, x, y)

        self.x_direction = x_dir
        self.forcing = x_dir

        self.jump_power = 0

    def update(self):
        pass

    def draw(self):
        self.clip_draw()

        if self.show_bb:
            self.draw_bb()

    def handle_event(self):
        pass


class Goomba(Enemy):
    def __init__(self, x=0, y=0, x_dir=DIR.RIGHT):
        super().__init__(TID.GOOMBA, x, y, x_dir)

        self.velocity = get_pps_from_kmph(8)

        self.on_floor = True
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
        self.update_frame(gs_framework.frame_time)

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