from pico2d import *
from value import *
from abc import *
from bounding_box import *

D_NONE = 0
D_RIGHT = 1
D_LEFT = -1
D_UP = 1
D_DOWN = -1


class Object:
    image = None

    def __init__(self, type_name, type_id, state):
        # Image initialization
        if None == Object.image:
            Object.image = {
                (TN.PLAYER, TID.MARIO_SMALL): load_image('resource\\characters\\mario_small.png'),
                (TN.PLAYER, TID.MARIO_SUPER): load_image('resource\\characters\\mario_super.png'),
                (TN.TILESETS, TID.CASTLE_BLOCK_50X50): load_image('resource\\tileset\\block50x50.png'),
                (TN.TILESETS, TID.CASTLE_BLOCK_50X100): load_image('resource\\tileset\\block50x100.png'),
                (TN.TILESETS, TID.CASTLE_BLOCK_100X50): load_image('resource\\tileset\\block100x50.png'),
                (TN.TILESETS, TID.CASTLE_BLOCK_100X100): load_image('resource\\tileset\\block100x100.png'),
                (TN.ENEMIES, TID.GOOMBA): load_image('resource\\characters\\goomba.png'),
                (TN.ENEMIES, TID.DRY_BONES): load_image('resource\\characters\\dry_bones.png'),
                (TN.ENEMIES, TID.BOO): load_image('resource\\characters\\boo.png'),
                (TN.ENEMIES, TID.PIRANHA_PLANT): load_image('resource\\characters\\piranha_plant.png'),
                (TN.ENEMIES, TID.SPINNING_SPIKE): load_image('resource\\characters\\spinning_spike.png'),
                (TN.ITEMS, TID.COIN): load_image('resource\\items\\coin.png'),
                (TN.ITEMS, TID.FIRE_FLOWER): load_image('resource\\items\\fire_flower.png'),
                (TN.ITEMS, TID.LIFE_MUSHROOM): load_image('resource\\items\\life_mushroom.png'),
                (TN.ITEMS, TID.STAR_COIN): load_image('resource\\items\\starcoin.png'),
                (TN.ITEMS, TID.SUPER_MUSHROOM): load_image('resource\\items\\super_mushroom.png'),
                (TN.ITEMS, TID.SUPER_STAR): load_image('resource\\items\\super_star.png')
            }

        # Object location point
        self.x, self.y = 0, 0
        self.px, self.py = self.x, self.y

        # Bounding Box
        self.bounding_box = {}
        self.show_bb = False

        # Object moving value
        self.max_velocity = 0
        self.velocity = 0
        self.jump_power = 0
        self.accel = 0

        # Animation sprite value
        self.l, self.b, self.w, self.h = 0, 0, 0, 0

        # Animation Direction
        self.facing = D_RIGHT
        self.x_direction = D_NONE
        self.y_direction = D_NONE
        self.forcing = D_NONE

        # Object Type
        self.type_name = type_name
        self.type_id = type_id

        # Object action with sprite animation
        self.action = ACTION.IDLE

        # Event and state
        self.event_que = []
        self.cur_state = state

        # Animation frame value
        self.time_per_action = 0.0
        self.action_per_time = 0.0
        self.frame = 0
        self.frame_begin = 0
        self.frame_count = 0

        # Animation control value
        self.loop_animation = False

    def set_tpa(self, tpa):
        self.time_per_action = tpa
        self.action_per_time = 1.0 / self.time_per_action

    def draw(self):
        Object.image[(self.type_name, self.type_id)].draw(self.x, self.y)

    def clip_draw(self):
        if self.frame_count == 1:
            self.frame = 0

        Object.image[(self.type_name, self.type_id)].clip_draw(
            int((self.frame + self.frame_begin)) * self.l, self.b,
            self.w, self.h, self.x, self.y)

    def draw_bb(self):
        for key in self.bounding_box.keys():
            self.bounding_box[key].draw_bb((self.x, self.y))

    @abstractmethod
    def update(self):
        pass

    def update_frame(self, frame_time):
        if self.frame_count == 0:
            self.frame_count = 1
            print("count value error")

        if self.frame_count == 1:
            return

        if not self.loop_animation:
            if self.frame + 1 == self.frame_count:
                return

        self.frame = (self.frame +
                      self.frame_count *
                      self.action_per_time *
                      frame_time
                      ) % self.frame_count

    def set_clip(self, a=None):

        if a == self.action:
            return

        if a != None:
            self.action = a

        if (self.type_name, self.type_id) == (TN.PLAYER, TID.MARIO_SMALL):
            self.correction_y = 15
            self.bounding_box[HB.COLLISION] = BoundingBox(HB.COLLISION)
            self.bounding_box[HB.STAND] = BoundingBox(HB.STAND)
            self.bounding_box[HB.ATTACK] = BoundingBox(HB.ATTACK)
            self.bounding_box[HB.BREAK] = BoundingBox(HB.BREAK)

            if self.action == ACTION.IDLE and self.facing == D_RIGHT:
                self.set_tpa(1.2)
                self.l, self.b, self.w, self.h = 50, 50 * 9, 50, 50
                self.frame_count, self.frame_begin = 27, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((13, 15, 13, 22))
                self.bounding_box[HB.STAND].set_bb((-14, 15, 12, 12))
                self.loop_animation = True
            elif self.action == ACTION.IDLE and self.facing == D_LEFT:
                self.set_tpa(1.2)
                self.l, self.b, self.w, self.h = 50, 50 * 8, 50, 50
                self.frame_count, self.frame_begin = 27, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((22, 15, 13, 13))
                self.bounding_box[HB.STAND].set_bb((-14, 15, 12, 12))
                self.loop_animation = True
            elif self.action == ACTION.WALK and self.facing == D_RIGHT:
                self.set_tpa(1.2)
                self.l, self.b, self.w, self.h = 50, 50 * 7, 50, 50
                self.frame_count, self.frame_begin = 18, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((22, 15, 13, 13))
                self.bounding_box[HB.STAND].set_bb((-14, 15, 12, 12))
                self.loop_animation = True
            elif self.action == ACTION.WALK and self.facing == D_LEFT:
                self.set_tpa(1.2)
                self.l, self.b, self.w, self.h = 50, 50 * 6, 50, 50
                self.frame_count, self.frame_begin = 18, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((22, 15, 13, 13))
                self.bounding_box[HB.STAND].set_bb((-14, 15, 12, 12))
                self.loop_animation = True
            elif self.action == ACTION.RUN and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((13, 15, 20, 22))
                self.bounding_box[HB.STAND].set_bb((12, 15, 18, -14))
                self.loop_animation = True
            elif self.action == ACTION.RUN and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 4, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((20, 15, 13, 22))
                self.bounding_box[HB.STAND].set_bb((18, 15, 12, -14))
                self.loop_animation = True
            elif self.action == ACTION.BREAK and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 4, 50, 50
                self.frame_count, self.frame_begin = 1, 8
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((13, 15, 20, 22))
                self.bounding_box[HB.STAND].set_bb((12, 15, 18, -14))
                self.loop_animation = False
            elif self.action == ACTION.BREAK and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 1, 8
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((13, 15, 20, 22))
                self.bounding_box[HB.STAND].set_bb((12, 15, 18, -14))
                self.loop_animation = False
            elif self.action == ACTION.SWIM and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 9, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((13, 15, 20, 22))
                self.bounding_box[HB.STAND].set_bb((12, 15, 18, -14))
                self.loop_animation = True
            elif self.action == ACTION.SWIM and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 9, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((20, 15, 13, 22))
                self.bounding_box[HB.STAND].set_bb((18, 15, 12, -14))
                self.loop_animation = True
            elif self.action == ACTION.HANG:
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 6, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = False
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((13, 15, 13, 22))
                self.loop_animation = True
            elif self.action == ACTION.CLIMB:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 14, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((13, 15, 13, 22))
                self.bounding_box[HB.STAND].set_bb((12, 15, 12, -14))
                self.loop_animation = True
            elif self.action == ACTION.JUMP and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 7, 50, 50
                self.frame_count, self.frame_begin = 1, 18
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = False
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = True
                self.bounding_box[HB.COLLISION].set_bb((13, 15, 12, 22))
                self.bounding_box[HB.BREAK].set_bb((12, -23, 8, 25))
                self.loop_animation = False
            elif self.action == ACTION.FALL and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 7, 50, 50
                self.frame_count, self.frame_begin = 1, 19
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = True
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((12, 15, 12, 22))
                self.bounding_box[HB.STAND].set_bb((11, 15, 11, -14))
                self.bounding_box[HB.ATTACK].set_bb((8, 15, 16, -8))
                self.loop_animation = False
            elif self.action == ACTION.JUMP and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 6, 50, 50
                self.frame_count, self.frame_begin = 1, 18
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = False
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = True
                self.bounding_box[HB.COLLISION].set_bb((12, 15, 13, 22))
                self.bounding_box[HB.BREAK].set_bb((8, -23, 12, 25))
                self.loop_animation = False
            elif self.action == ACTION.FALL and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 6, 50, 50
                self.frame_count, self.frame_begin = 1, 19
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = True
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((12, 15, 12, 22))
                self.bounding_box[HB.STAND].set_bb((11, 15, 11, -14))
                self.bounding_box[HB.ATTACK].set_bb((16, 15, 8, -8))
                self.loop_animation = False
            elif self.action == ACTION.DIE_A:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 1, 14
                self.bounding_box[HB.COLLISION].is_on = False
                self.bounding_box[HB.STAND].is_on = False
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.loop_animation = False

            else:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 1, 26
                self.loop_animation = False

        elif (self.type_name, self.type_id) == (TN.PLAYER, TID.MARIO_SUPER):
            self.correction_y = 40
            self.bounding_box[HB.COLLISION] = BoundingBox(HB.COLLISION)
            self.bounding_box[HB.STAND] = BoundingBox(HB.STAND)
            self.bounding_box[HB.ATTACK] = BoundingBox(HB.ATTACK)
            self.bounding_box[HB.BREAK] = BoundingBox(HB.BREAK)

            if self.action == ACTION.IDLE and self.facing == D_RIGHT:
                self.set_tpa(1.2)
                self.l, self.b, self.w, self.h = 50, 100 * 9, 50, 100
                self.frame_count, self.frame_begin = 27, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((15, 40, 15, 30))
                self.bounding_box[HB.STAND].set_bb((14, 40, 14, -39))
                self.loop_animation = True
            elif self.action == ACTION.IDLE and self.facing == D_LEFT:
                self.set_tpa(1.2)
                self.l, self.b, self.w, self.h = 50, 100 * 8, 50, 100
                self.frame_count, self.frame_begin = 27, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((15, 40, 15, 30))
                self.bounding_box[HB.STAND].set_bb((14, 40, 14, -39))
                self.loop_animation = True
            elif self.action == ACTION.WALK and self.facing == D_RIGHT:
                self.set_tpa(1.0)
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 18, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((15, 40, 15, 30))
                self.bounding_box[HB.STAND].set_bb((14, 40, 14, -39))
                self.loop_animation = True
            elif self.action == ACTION.WALK and self.facing == D_LEFT:
                self.set_tpa(1.0)
                self.l, self.b, self.w, self.h = 50, 100 * 6, 50, 100
                self.frame_count, self.frame_begin = 18, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((15, 40, 15, 30))
                self.bounding_box[HB.STAND].set_bb((14, 40, 14, -39))
                self.loop_animation = True
            elif self.action == ACTION.RUN and self.facing == D_RIGHT:
                self.set_tpa(0.5)
                self.l, self.b, self.w, self.h = 100, 100 * 5, 100, 100
                self.frame_count, self.frame_begin = 8, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((25, 40, 25, 20))
                self.bounding_box[HB.STAND].set_bb((24, 40, 24, -39))
                self.loop_animation = True
            elif self.action == ACTION.RUN and self.facing == D_LEFT:
                self.set_tpa(0.5)
                self.l, self.b, self.w, self.h = 100, 100 * 4, 100, 100
                self.frame_count, self.frame_begin = 8, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((25, 40, 25, 20))
                self.bounding_box[HB.STAND].set_bb((24, 40, 24, -39))
                self.loop_animation = True
            elif self.action == ACTION.BREAK and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 4, 100, 100
                self.frame_count, self.frame_begin = 1, 8
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((25, 40, 25, 20))
                self.bounding_box[HB.STAND].set_bb((24, 40, 24, -39))
                self.loop_animation = False
            elif self.action == ACTION.BREAK and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 5, 100, 100
                self.frame_count, self.frame_begin = 1, 8
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((25, 40, 25, 20))
                self.bounding_box[HB.STAND].set_bb((24, 40, 24, -39))
                self.loop_animation = False
            elif self.action == ACTION.SWIM and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 3, 100, 100
                self.frame_count, self.frame_begin = 9, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((25, 40, 28, 21))
                self.bounding_box[HB.STAND].set_bb((24, 40, 27, -39))
                self.loop_animation = True
            elif self.action == ACTION.SWIM and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 2, 100, 100
                self.frame_count, self.frame_begin = 9, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((28, 40, 25, 21))
                self.bounding_box[HB.STAND].set_bb((27, 40, 24, -39))
                self.loop_animation = True
            elif self.action == ACTION.HANG:
                self.l, self.b, self.w, self.h = 50, 100 * 1, 50, 100
                self.frame_count, self.frame_begin = 6, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = False
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((15, 40, 15, 30))
                self.loop_animation = True
            elif self.action == ACTION.CLIMB:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 14, 0
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((15, 40, 15, 30))
                self.bounding_box[HB.STAND].set_bb((14, 40, 14, -39))
                self.loop_animation = True
            elif self.action == ACTION.SIT and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 9, 50, 100
                self.frame_count, self.frame_begin = 1, 27
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((15, 40, 15, -7))
                self.bounding_box[HB.STAND].set_bb((14, 40, 14, -39))
                self.loop_animation = False
            elif self.action == ACTION.SIT and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 8, 50, 100
                self.frame_count, self.frame_begin = 1, 27
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((15, 40, 15, -7))
                self.bounding_box[HB.STAND].set_bb((14, 40, 14, -39))
                self.loop_animation = False
            elif self.action == ACTION.JUMP and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 7, 100, 100
                self.frame_count, self.frame_begin = 1, 18 // 2
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = False
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = True
                self.bounding_box[HB.COLLISION].set_bb((15, 36, 15, 30))
                self.bounding_box[HB.BREAK].set_bb((15, -30, 15, 30))
                self.loop_animation = False
            elif self.action == ACTION.FALL and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 7, 100, 100
                self.frame_count, self.frame_begin = 1, 20 // 2
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = True
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((15, 40, 15, 30))
                self.bounding_box[HB.STAND].set_bb((14, 40, 14, -39))
                self.bounding_box[HB.ATTACK].set_bb((12, 41, 28, -32))
                self.loop_animation = False
            elif self.action == ACTION.JUMP and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 6, 100, 100
                self.frame_count, self.frame_begin = 1, 18 // 2
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = False
                self.bounding_box[HB.ATTACK].is_on = False
                self.bounding_box[HB.BREAK].is_on = True
                self.bounding_box[HB.COLLISION].set_bb((15, 36, 15, 30))
                self.bounding_box[HB.BREAK].set_bb((15, -30, 15, 30))
                self.loop_animation = False
            elif self.action == ACTION.FALL and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 6, 100, 100
                self.frame_count, self.frame_begin = 1, 20 // 2
                self.bounding_box[HB.COLLISION].is_on = True
                self.bounding_box[HB.STAND].is_on = True
                self.bounding_box[HB.ATTACK].is_on = True
                self.bounding_box[HB.BREAK].is_on = False
                self.bounding_box[HB.COLLISION].set_bb((15, 40, 15, 30))
                self.bounding_box[HB.STAND].set_bb((14, 40, 14, -39))
                self.bounding_box[HB.ATTACK].set_bb((28, 41, 12, -32))
                self.loop_animation = False

            else:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 1, 29
                self.loop_animation = False

        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.DRY_BONES):
            self.correction_y = 40

            if self.action == "stay" and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "stay" and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 6, 50, 100
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "walk" and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 5, 50, 100
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True
            elif self.action == "walk" and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 4, 50, 100
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True
            elif self.action == "break" and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 3, 50, 100
                self.frame_count, self.frame_begin = 12, 0
                self.loop_animation = False
            elif self.action == "break" and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 2, 50, 100
                self.frame_count, self.frame_begin = 12, 0
                self.loop_animation = False
            elif self.action == "restore" and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 1, 50, 100
                self.frame_count, self.frame_begin = 15, 0
                self.loop_animation = False
            elif self.action == "restore" and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 15, 0
                self.loop_animation = False
            else:
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 1, 15
                self.loop_animation = False

        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.GOOMBA):

            if self.action == "stay" and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "stay" and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 4, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "walk" and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True
            elif self.action == "walk" and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True
            elif self.action == "dieA":
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 3, 0
                self.loop_animation = False
            elif self.action == "dieB":
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            else:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 1, 15
                self.loop_animation = False

        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.BOO):
            if self.action == "stay" and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "stay" and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "fly" and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True
            elif self.action == "fly" and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True
            elif self.action == "die" and self.facing == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 1
                self.loop_animation = False
            elif self.action == "die" and self.facing == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 1, 1
                self.loop_animation = False
            else:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 7
                self.loop_animation = False

        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.PIRANHA_PLANT):
            if self.action == "pop":
                self.frame_count, self.frame_begin = 78, 0
                self.l, self.b, self.w, self.h = 50, 100 * 4, 50, 50
                self.loop_animation = False

        self.frame = self.frame_begin


def test_object():
    open_canvas()
    object = Object()



if __name__ == "__main__":
    test_object()