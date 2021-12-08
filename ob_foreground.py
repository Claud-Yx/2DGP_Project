import random

from pico2d import *
import game_object
import gs_framework
import ob_map
import object_manager
import server

from value import *

MIN_BRICK_PIECE_RAD_RPS = 360
MAX_BRICK_PIECE_RAD_RPS = 360 * 3
STEP_BRICK_PIECE_RAD_RPS = 90

MIN_BP_VELOCITY = int(get_pps_from_kmph(7.0))
MAX_BP_VELOCITY = int(get_pps_from_kmph(15.0))

MAX_JUMP_POWER = int(get_pps_from_mps(25))
MIN_JUMP_POWER = int(get_pps_from_mps(20))


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

        self.set_clip()

        if not isinstance(self, BrickPiece):
            self.ax = x * ob_map.TILE_WIDTH + game_object.GameObject.image[self.pm_type_name, self.pm_type_id].w // 2
            self.ay = y * ob_map.TILE_HEIGHT + game_object.GameObject.image[self.pm_type_name, self.pm_type_id].h // 2

    def update(self):
        pass

    def draw(self):
        server.move_camera(self)

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

        if self.action == ACTION.PIECE_LB or self.action == ACTION.PIECE_LT:
            self.x_direction = DIR.LEFT
        elif self.action == ACTION.PIECE_RT or self.action == ACTION.PIECE_RB:
            self.x_direction = DIR.RIGHT

        self.velocity = random.randrange(MIN_BP_VELOCITY, MAX_BP_VELOCITY)
        self.jump_power = random.randrange(MIN_JUMP_POWER, MAX_JUMP_POWER)
        self.rps = random.randrange(MIN_BRICK_PIECE_RAD_RPS, MAX_BRICK_PIECE_RAD_RPS, STEP_BRICK_PIECE_RAD_RPS)

    def jump(self):
        self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 6
                            ) * -1

        self.ay += self.jump_power * gs_framework.frame_time

    def fall(self):
        self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 6
                            ) * -1

        self.jump_power = clamp(-MAX_JUMP_POWER * 2, self.jump_power, 0)

        self.ay += self.jump_power * gs_framework.frame_time

    def update(self):
        if server.time_stop:
            return

        if self.ay <= -50:
            object_manager.remove_object(self)
            del self
            return

        if self.jump_power > 0:
            self.jump()
        else:
            self.fall()

        self.rad += self.rps * gs_framework.frame_time * -self.x_direction
        self.ax += self.velocity * gs_framework.frame_time * self.x_direction


    def draw(self):
        server.move_camera(self)

        self.update_frame(gs_framework.frame_time)
        self.clip_draw(self.pm_type_name, self.pm_type_id, self.rad)

