import object_manager
from game_object import *
from value import *

import gs_framework
import game_object

import server

MAX_JUMP_POWER = get_pps_from_mps(20)
MAX_FLYING_DEAD_VELOCITY = get_pps_from_kmph(10)
GOOMBA_MAX_VELOCITY = get_pps_from_kmph(8)
DRYBONES_MAX_VELOCITY = get_pps_from_kmph(8)

DRYBONES_MAX_TIMER_DIE_A = 4
DRYBONES_MAX_TIMER_RESTORE = 1.3


class Enemy(game_object.GameObject, ABC):
    def __init__(self, tid=TID.NONE, x=0, y=0, x_dir=DIR.RIGHT):
        super().__init__(TN.ENEMIES, tid, x, y)

        self.x_direction = x_dir
        self.facing = x_dir
        self.dead_type = None

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


class DryBones(Enemy, ABC):
    def __init__(self, x=0, y=0, x_dir=DIR.RIGHT):
        super().__init__(TID.DRY_BONES, x, y, x_dir)

        del self.timer

        self.hp, self.wp = 1.2, 1.2

        self.velocity = DRYBONES_MAX_VELOCITY

        self.on_floor = False
        self.is_fall = False
        self.is_jump = False

        self.timer_die_a = 0.0
        self.timer_restore = 0.0

        self.set_info(ACTION.WALK)

    def jump(self):

        if self.dead_type is None:
            self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                                ) * -1
        else:
            self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 6
                                ) * -1

        self.jump_power = clamp(
            0, self.jump_power, MAX_JUMP_POWER
        )

        if self.jump_power == 0:
            self.is_fall = True
            self.is_jump = False

        self.ay += self.jump_power * gs_framework.frame_time

    def fall(self):
        if self.dead_type is None:
            self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                                ) * -1
        else:
            self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 6
                                ) * -1

        self.jump_power = clamp(
            MAX_JUMP_POWER * -2, self.jump_power, 0
        )

        self.ay += self.jump_power * gs_framework.frame_time

    def die(self) -> bool:
        if self.dead_type == ACTION.DIE_A:

            if self.timer_die_a == 0:
                self.timer_die_a = DRYBONES_MAX_TIMER_DIE_A
                self.set_info(ACTION.DIE_A)

            self.timer_die_a -= gs_framework.frame_time

            if self.timer_die_a <= 0.0:
                self.timer_die_a = 0.0
                self.dead_type = ACTION.RESTORE

        elif self.dead_type == ACTION.RESTORE:

            if self.timer_restore == 0:
                self.timer_restore = DRYBONES_MAX_TIMER_RESTORE
                self.set_info(ACTION.RESTORE)

            self.timer_restore -= gs_framework.frame_time

            if self.timer_restore <= 0.0:
                self.timer_restore = 0.0
                self.dead_type = None
                self.action = ACTION.WALK

        elif self.dead_type == ACTION.DIE_B:
            self.set_info(ACTION.DIE_B)
            if not self.is_jump and self.on_floor:
                self.is_jump = True
                self.is_fall = False
                self.on_floor = False
                self.jump_power = MAX_JUMP_POWER
                self.ay += 10
                self.x_direction = server.player.facing * -1

            self.ax += MAX_FLYING_DEAD_VELOCITY * gs_framework.frame_time * self.x_direction

            if self.is_jump:
                self.jump()
            elif self.is_fall:
                self.fall()

    def update(self):
        if self.is_time_stop:
            return

        if self.ay <= server.stage.y - ob_map.TILE_WIDTH:
            object_manager.remove_object(self)
            del self
            return

        self.update_frame(gs_framework.frame_time)

        if self.dead_type is not None:
            self.die()

        if not self.on_floor and not self.is_fall and not self.dead_type == ACTION.DIE_B:
            self.is_fall = True

        if self.is_fall and not self.dead_type == ACTION.DIE_B:
            self.on_floor = False
            self.fall()

        # print(str(self.facing), str(self.x_direction), str(self.action), str(self.velocity))
        if self.dead_type is None:
            self.ax += self.velocity * gs_framework.frame_time * self.x_direction


class Goomba(Enemy, ABC):
    def __init__(self, x=0, y=0, x_dir=DIR.RIGHT):
        super().__init__(TID.GOOMBA, x, y, x_dir)

        self.velocity = GOOMBA_MAX_VELOCITY

        self.on_floor = False
        self.is_fall = False
        self.is_jump = False

        self.set_info(ACTION.WALK)

    def jump(self):

        if self.dead_type is None:
            self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                                ) * -1
        else:
            self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 6
                                ) * -1

        self.jump_power = clamp(
            0, self.jump_power, MAX_JUMP_POWER
        )

        if self.jump_power == 0:
            self.is_fall = True
            self.is_jump = False

        self.ay += self.jump_power * gs_framework.frame_time

    def fall(self):
        if self.dead_type is None:
            self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                                ) * -1
        else:
            self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 6
                                ) * -1

        self.jump_power = clamp(
            MAX_JUMP_POWER * -2, self.jump_power, 0
        )

        self.ay += self.jump_power * gs_framework.frame_time

    def die(self) -> bool:
        if self.dead_type == ACTION.DIE_A:
            self.set_info(ACTION.DIE_A)

            if self.timer == 0:
                self.timer = 1.0

            self.timer -= gs_framework.frame_time

            if self.timer <= 0.0:
                return True

        elif self.dead_type == ACTION.DIE_B:
            self.set_info(ACTION.DIE_B)
            if not self.is_jump and self.on_floor:
                self.is_jump = True
                self.is_fall = False
                self.on_floor = False
                self.jump_power = MAX_JUMP_POWER
                self.ay += 10
                self.x_direction = server.player.facing * -1

            self.ax += MAX_FLYING_DEAD_VELOCITY * gs_framework.frame_time * self.x_direction

            if self.is_jump:
                self.jump()
            elif self.is_fall:
                self.fall()

        return False

    def update(self):
        if self.is_time_stop:
            return


        # print("enemy - is_jump: %s / is_fall: %s / on_floor %s" % (self.is_jump, self.is_fall, self.on_floor))

        if self.ay <= server.stage.y - ob_map.TILE_WIDTH:
            object_manager.remove_object(self)
            del self
            return

        self.update_frame(gs_framework.frame_time)

        if self.dead_type is not None:
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
        self.ax += self.velocity * gs_framework.frame_time * self.x_direction


def test_enemy():
    from ob_tileset import TileSet

    open_canvas()
    goomba = Goomba()


if __name__ == "__main__":
    test_enemy()
