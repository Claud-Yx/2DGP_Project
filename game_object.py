from pico2d import *

import ob_foreground
import ob_interactive
import ob_map
from value import *
from abc import *
from bounding_box import *


class GameObject:
    image = None

    def __init__(self, type_name, type_id, x=0, y=0):
        # Image initialization
        if None == GameObject.image:
            GameObject.image = {
                (TN.PLAYER, TID.MARIO_SMALL): load_image('resource\\characters\\mario_small.png'),
                (TN.PLAYER, TID.MARIO_SUPER): load_image('resource\\characters\\mario_super.png'),
                (TN.TILESETS, TID.CASTLE_BLOCK_50X50): load_image('resource\\tileset\\block50x50.png'),
                (TN.TILESETS, TID.CASTLE_BLOCK_50X100): load_image('resource\\tileset\\block50x100.png'),
                (TN.TILESETS, TID.CASTLE_BLOCK_100X50): load_image('resource\\tileset\\block100x50.png'),
                (TN.TILESETS, TID.CASTLE_BLOCK_100X100): load_image('resource\\tileset\\block100x100.png'),
                (TN.TILESETS, TID.EMPTY_BOX): load_image('resource\\tileset\\empty_box50x50.png'),
                (TN.TILESETS, TID.BREAKABLE_BRICK): load_image('resource\\tileset\\breakable_brick50x50.png'),
                (TN.TILESETS, TID.RANDOM_BOX): load_image('resource\\tileset\\random_box50x50.png'),
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
                (TN.ITEMS, TID.SUPER_STAR): load_image('resource\\items\\super_star.png'),
                (TN.INTERACTIVES, TID.WIRE_MESH): load_image('resource\\interactives\\wire_mesh150x150.png'),
                (TN.FOREGROUND, TID.BRICK_PIECE): load_image('resource\\foreground\\brick_piece25x25.png'),
                TID.NONE: load_image('resource\\no_image.png')
            }

        # Object location point
        self.x, self.y = x, y

        # Bounding Box
        self.bounding_box: Dict[int, BoundingBox] = {}
        self.bb_size_range = [0, 0, 0, 0]
        self.show_bb = False

        # Object moving value
        self.max_velocity = 0
        self.velocity = 0

        # Animation sprite value
        self.l, self.b, self.w, self.h = 0, 0, 0, 0
        self.wp, self.hp = 1.0, 1.0
        self.rad = 0

        # Animation Direction
        self.facing = DIR.RIGHT
        self.x_direction = DIR.NONE
        self.y_direction = DIR.NONE
        self.forcing = DIR.NONE

        # Object Type
        self.type_name = type_name
        self.type_id = type_id

        # Object action with sprite animation
        self.action = ACTION.IDLE

        # Animation frame value
        self.time_per_action = 0.0
        self.action_per_time = 0.0
        self.frame = 0
        self.frame_begin = 0
        self.frame_count = 0

        # Animation control value
        self.loop_animation = False

        # Time stop
        self.is_time_stop = False

    def set_alpha(self, a=255):
        """Setting alpha value to image"""
        if self.type_name == TN.FOREGROUND:
            SDL_SetTextureAlphaMod(GameObject.image[self.pm_type_name, self.pm_type_id].texture, a)
        else:
            SDL_SetTextureAlphaMod(GameObject.image[self.type_name, self.type_id].texture, a)

    def set_tpa(self, tpa):
        self.time_per_action = tpa
        self.action_per_time = 1.0 / self.time_per_action

    def image_draw(self, tn=None, tid=None, rad=None):
        if tn is None:
            tn = self.type_name
        if tid is None:
            tid = self.type_id
        if rad is None:
            rad = self.rad

        if self.type_id == TID.NONE:
            GameObject.image[tid].draw(self.x, self.y, self.w * self.wp, self.h * self.hp)
        else:
            if rad == 0:
                GameObject.image[(tn, tid)].draw(
                    self.x, self.y,
                    GameObject.image[(tn, tid)].w * self.wp,
                    GameObject.image[(tn, tid)].h * self.hp)
            else:
                GameObject.image[(tn, tid)].composite_draw(
                    rad, '', self.x, self.y,
                    GameObject.image[(tn, tid)].w * self.wp,
                    GameObject.image[(tn, tid)].h * self.hp)

        self.set_alpha()

    def clip_draw(self, tn=None, tid=None, rad=None):
        if tn is None:
            tn = self.type_name
        if tid is None:
            tid = self.type_id
        if rad is None:
            rad = self.rad

        if tid == TID.NONE:
            GameObject.image[tid].draw(
                self.x, self.y, self.w * self.wp, self.h * self.hp)
            return

        if self.frame_count == 1:
            self.frame = 0

        if rad == 0:
            GameObject.image[(tn, tid)].clip_draw(
                int((self.frame + self.frame_begin)) * self.l, self.b,
                self.w, self.h, self.x, self.y, self.w * self.wp, self.h * self.hp)
        else:
            GameObject.image[(tn, tid)].clip_composite_draw(
                int((self.frame + self.frame_begin)) * self.l, self.b,
                self.w, self.h,
                rad*(math.pi/180), '',
                self.x, self.y, self.w * self.wp, self.h * self.hp)

        self.set_alpha()

    def set_size(self, wp=1.0, hp=1.0, set_now=True):
        self.wp = wp
        self.hp = hp

        if set_now:
            self.set_info()

    def get_bb_range(self, bid):
        return self.bounding_box[bid].range

    def get_bb_on(self, bid):
        return self.bounding_box[bid].is_on

    def set_bb_on(self, bid, b=True):
        self.bounding_box[bid].is_on = b
        return self.bounding_box[bid].is_on

    def set_bb(self, bid, range: List[int]):
        if not self.bounding_box[bid].is_on:
            self.bounding_box[bid].is_on = True

        if self.wp != 1.0:
            range[POS.LEFT] *= self.wp
            range[POS.RIGHT] *= self.wp

        if self.hp != 1.0:
            range[POS.BOTTOM] *= self.hp
            range[POS.TOP] *= self.hp

        self.bounding_box[bid].set_bb(range)

    def get_bb(self, bid):
        return self.bounding_box[bid].get_bb((self.x, self.y))

    def draw_bb(self):
        for key in self.bounding_box.keys():
            self.bounding_box[key].draw_bb((self.x, self.y))

    def set_bb_size(self):
        self.bb_size_range = [0, 0, 0, 0]

        for key in self.bounding_box.keys():
            bb_range = self.get_bb_range(key)
            if self.bb_size_range[POS.LEFT] < bb_range[POS.LEFT]:
                self.bb_size_range[POS.LEFT] = bb_range[POS.LEFT]
            if self.bb_size_range[POS.BOTTOM] < bb_range[POS.BOTTOM]:
                self.bb_size_range[POS.BOTTOM] = bb_range[POS.BOTTOM]
            if self.bb_size_range[POS.RIGHT] < bb_range[POS.RIGHT]:
                self.bb_size_range[POS.RIGHT] = bb_range[POS.RIGHT]
            if self.bb_size_range[POS.TOP] < bb_range[POS.TOP]:
                self.bb_size_range[POS.TOP] = bb_range[POS.TOP]

    def get_bb_size_pos(self) -> Tuple[float, float, float, float]:
        return (
            self.x - self.bb_size_range[POS.LEFT],
            self.y - self.bb_size_range[POS.BOTTOM],
            self.x + self.bb_size_range[POS.RIGHT],
            self.y + self.bb_size_range[POS.TOP]
        )

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    def update_frame(self, frame_time):
        if self.frame_count == 0:
            self.frame_count = 1
            print("count value error")

        if self.frame_count == 1:
            return

        if not self.loop_animation:
            if self.frame + 1 >= self.frame_count:
                return

        self.frame = (self.frame +
                      self.frame_count *
                      self.action_per_time *
                      frame_time
                      ) % self.frame_count

    def switch_bb_all(self, b=False):
        for key in self.bounding_box.keys():
            self.bounding_box[key].is_on = b

    def init_bb(self):
        if (self.type_name, self.type_id) == (TN.PLAYER, TID.MARIO_SMALL):
            if len(self.bounding_box) == 0:
                self.bounding_box[HB.BODY] = BoundingBox(HB.BODY)
                self.bounding_box[HB.LEFT] = BoundingBox(HB.LEFT)
                self.bounding_box[HB.BOTTOM] = BoundingBox(HB.BOTTOM)
                self.bounding_box[HB.RIGHT] = BoundingBox(HB.RIGHT)
                self.bounding_box[HB.TOP] = BoundingBox(HB.TOP)
            self.switch_bb_all()
            self.set_size(1.2, 1.2, False)

            # Idle right
            if self.action == ACTION.IDLE and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [13, 15, 13, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 13, 22])

            # Idle left
            elif self.action == ACTION.IDLE and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [13, 15, 13, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 13, 22])

            # Walk right
            elif self.action == ACTION.WALK and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [13, 15, 13, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 13, 22])

            # Walk left
            elif self.action == ACTION.WALK and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [13, 15, 13, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 13, 22])

            # Run right
            elif self.action == ACTION.RUN and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [13, 15, 18, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 18, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 18, 22])

            # Run left
            elif self.action == ACTION.RUN and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [18, 15, 13, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [18, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [18, -21, 13, 22])

            # Break right
            elif self.action == ACTION.BREAK and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [13, 15, 18, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 18, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 18, 22])

            # Break left
            elif self.action == ACTION.BREAK and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [18, 15, 13, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [18, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [18, -21, 13, 22])

            # Swim right
            elif self.action == ACTION.SWIM and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [13, 15, 18, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 18, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 18, 22])

            # Swim Left
            elif self.action == ACTION.SWIM and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [18, 15, 13, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [18, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [18, -21, 13, 22])

            # Hang
            elif self.action == ACTION.HANG:
                self.set_bb(HB.BODY, [13, 15, 13, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 13, 22])

            # Climb
            elif self.action == ACTION.CLIMB:
                self.set_bb(HB.BODY, [13, 15, 13, 22])
                self.set_bb(HB.LEFT, [13, 15, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 13, 22])

            # Jump right
            elif self.action == ACTION.JUMP and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [13, 15, 13, 18])
                self.set_bb(HB.LEFT, [13, 15, -12, 18])
                self.set_bb(HB.BOTTOM, [13, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 18])
                self.set_bb(HB.TOP, [12, -21, 12, 22])

            # Jump left
            elif self.action == ACTION.JUMP and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [13, 15, 13, 18])
                self.set_bb(HB.LEFT, [13, 15, -12, 18])
                self.set_bb(HB.BOTTOM, [13, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 15, 13, 18])
                self.set_bb(HB.TOP, [12, -21, 12, 22])

            # Fall right
            elif self.action == ACTION.FALL and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [13, 10, 13, 22])
                self.set_bb(HB.LEFT, [13, 10, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 10, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 13, 22])

            # Fall left
            elif self.action == ACTION.FALL and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [13, 10, 13, 22])
                self.set_bb(HB.LEFT, [13, 10, -12, 22])
                self.set_bb(HB.BOTTOM, [13, 15, 13, -14])
                self.set_bb(HB.RIGHT, [-12, 10, 13, 22])
                self.set_bb(HB.TOP, [13, -21, 13, 22])

            elif self.action == ACTION.SIT:
                self.switch_bb_all(True)

            # Die A
            elif self.action == ACTION.DIE_A:
                pass

            else:
                print("Invalid action: %s" % (str(self.action)))
                exit(-1)

        # Mario_Super
        elif (self.type_name, self.type_id) == (TN.PLAYER, TID.MARIO_SUPER):
            if len(self.bounding_box) == 0:
                self.bounding_box[HB.BODY] = BoundingBox(HB.BODY)
                self.bounding_box[HB.LEFT] = BoundingBox(HB.LEFT)
                self.bounding_box[HB.BOTTOM] = BoundingBox(HB.BOTTOM)
                self.bounding_box[HB.RIGHT] = BoundingBox(HB.RIGHT)
                self.bounding_box[HB.TOP] = BoundingBox(HB.TOP)
            self.switch_bb_all()

            # Idle right
            if self.action == ACTION.IDLE and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [15, 40, 15, 30])
                self.set_bb(HB.LEFT, [15, 40, -14, 30])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 30])
                self.set_bb(HB.TOP, [15, -29, 15, 30])

            # Idle left
            elif self.action == ACTION.IDLE and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [15, 40, 15, 30])
                self.set_bb(HB.LEFT, [15, 40, -14, 30])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 30])
                self.set_bb(HB.TOP, [15, -29, 15, 30])

            # Walk right
            elif self.action == ACTION.WALK and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [15, 40, 15, 30])
                self.set_bb(HB.LEFT, [15, 40, -14, 30])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 30])
                self.set_bb(HB.TOP, [15, -29, 15, 30])

            # Walk left
            elif self.action == ACTION.WALK and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [15, 40, 15, 30])
                self.set_bb(HB.LEFT, [15, 40, -14, 30])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 30])
                self.set_bb(HB.TOP, [15, -29, 15, 30])

            # Run right
            elif self.action == ACTION.RUN and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [25, 40, 25, 20])
                self.set_bb(HB.LEFT, [15, 40, -14, 20])
                self.set_bb(HB.BOTTOM, [25, 40, 25, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 20])
                self.set_bb(HB.TOP, [25, -19, 25, 20])

            # Run left
            elif self.action == ACTION.RUN and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [25, 40, 25, 20])
                self.set_bb(HB.LEFT, [15, 40, -14, 20])
                self.set_bb(HB.BOTTOM, [25, 40, 25, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 20])
                self.set_bb(HB.TOP, [25, -19, 25, 20])

            # Break right
            elif self.action == ACTION.BREAK and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [25, 40, 25, 20])
                self.set_bb(HB.LEFT, [15, 40, -14, 20])
                self.set_bb(HB.BOTTOM, [25, 40, 25, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 20])
                self.set_bb(HB.TOP, [25, -19, 25, 20])

            # Break left
            elif self.action == ACTION.BREAK and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [25, 40, 25, 20])
                self.set_bb(HB.LEFT, [15, 40, -14, 20])
                self.set_bb(HB.BOTTOM, [25, 40, 25, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 20])
                self.set_bb(HB.TOP, [25, -19, 25, 20])

            # Swim right
            elif self.action == ACTION.SWIM and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [25, 40, 25, 20])
                self.set_bb(HB.LEFT, [15, 40, -14, 20])
                self.set_bb(HB.BOTTOM, [25, 40, 25, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 20])
                self.set_bb(HB.TOP, [25, -19, 25, 20])

            # Swim left
            elif self.action == ACTION.SWIM and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [25, 40, 25, 20])
                self.set_bb(HB.LEFT, [15, 40, -14, 20])
                self.set_bb(HB.BOTTOM, [25, 40, 25, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 20])
                self.set_bb(HB.TOP, [25, -19, 25, 20])

            # Hang
            elif self.action == ACTION.HANG:
                self.set_bb(HB.BODY, [15, 40, 15, 30])
                self.set_bb(HB.LEFT, [15, 40, -14, 30])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 30])
                self.set_bb(HB.TOP, [15, -29, 15, 30])

            # Climb
            elif self.action == ACTION.CLIMB:
                self.set_bb(HB.BODY, [15, 40, 15, 30])
                self.set_bb(HB.LEFT, [15, 40, -14, 30])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 30])
                self.set_bb(HB.TOP, [15, -29, 15, 30])

            # Sit right
            elif self.action == ACTION.SIT and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [15, 40, 15, -7])
                self.set_bb(HB.LEFT, [15, 40, -14, -7])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, -7])
                self.set_bb(HB.TOP, [15, 8, 15, -7])

            # Sit left
            elif self.action == ACTION.SIT and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [15, 40, 15, -7])
                self.set_bb(HB.LEFT, [15, 40, -14, -7])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, -7])
                self.set_bb(HB.TOP, [15, 8, 15, -7])

            # Jump right
            elif self.action == ACTION.JUMP and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [15, 40, 15, 30])
                self.set_bb(HB.LEFT, [15, 40, -14, 30])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 30])
                self.set_bb(HB.TOP, [14, -29, 14, 34])

            # Jump left
            elif self.action == ACTION.JUMP and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [15, 40, 15, 30])
                self.set_bb(HB.LEFT, [15, 40, -14, 30])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -39])
                self.set_bb(HB.RIGHT, [-14, 40, 15, 30])
                self.set_bb(HB.TOP, [14, -29, 14, 34])

            # Fall right
            elif self.action == ACTION.FALL and self.facing == DIR.RIGHT:
                self.set_bb(HB.BODY, [15, 35, 15, 30])
                self.set_bb(HB.LEFT, [15, 35, -14, 30])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -34])
                self.set_bb(HB.RIGHT, [-14, 35, 15, 30])
                self.set_bb(HB.TOP, [15, -29, 15, 30])

            # Fall left
            elif self.action == ACTION.FALL and self.facing == DIR.LEFT:
                self.set_bb(HB.BODY, [15, 35, 15, 30])
                self.set_bb(HB.LEFT, [15, 35, -14, 30])
                self.set_bb(HB.BOTTOM, [15, 40, 15, -34])
                self.set_bb(HB.RIGHT, [-14, 35, 15, 30])
                self.set_bb(HB.TOP, [15, -29, 15, 30])

            else:
                print("Invalid action: %s" % (str(self.action)))
                exit(-1)

        # Dry bones
        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.DRY_BONES):
            if len(self.bounding_box) == 0:
                self.bounding_box[HB.BODY] = BoundingBox(HB.BODY)
                self.bounding_box[HB.LEFT] = BoundingBox(HB.LEFT)
                self.bounding_box[HB.BOTTOM] = BoundingBox(HB.BOTTOM)
                self.bounding_box[HB.RIGHT] = BoundingBox(HB.RIGHT)
                self.bounding_box[HB.TOP] = BoundingBox(HB.TOP)
            self.switch_bb_all()

            # Idle right
            if self.action == ACTION.IDLE and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            # Idle left
            elif self.action == ACTION.IDLE and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 6, 50, 100
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            # Walk right
            elif self.action == ACTION.WALK and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 5, 50, 100
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True

            # Walk left
            elif self.action == ACTION.WALK and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 4, 50, 100
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True

            # Break right
            elif self.action == ACTION.BREAK and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 3, 50, 100
                self.frame_count, self.frame_begin = 12, 0
                self.loop_animation = False

            # Break left
            elif self.action == ACTION.BREAK and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 2, 50, 100
                self.frame_count, self.frame_begin = 12, 0
                self.loop_animation = False

            # Restore right
            elif self.action == ACTION.RESTORE and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 1, 50, 100
                self.frame_count, self.frame_begin = 15, 0
                self.loop_animation = False

            # Restore left
            elif self.action == ACTION.RESTORE and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 15, 0
                self.loop_animation = False

            else:
                print("Invalid action: %s" % (str(self.action)))
                exit(-1)

        # Goomba
        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.GOOMBA):
            if len(self.bounding_box) == 0:
                self.bounding_box[HB.BODY] = BoundingBox(HB.BODY)
                self.bounding_box[HB.LEFT] = BoundingBox(HB.LEFT)
                self.bounding_box[HB.BOTTOM] = BoundingBox(HB.BOTTOM)
                self.bounding_box[HB.RIGHT] = BoundingBox(HB.RIGHT)
                self.bounding_box[HB.TOP] = BoundingBox(HB.TOP)
            self.switch_bb_all()

            # Idle right or Idle left or Walk right or Walk left
            if (self.action == ACTION.IDLE and self.facing == DIR.RIGHT or
                    self.action == ACTION.IDLE and self.facing == DIR.LEFT or
                    self.action == ACTION.WALK and self.facing == DIR.RIGHT or
                    self.action == ACTION.WALK and self.facing == DIR.LEFT
            ):
                self.set_bb(HB.BODY, [21, 25, 21, 21])
                self.set_bb(HB.LEFT, [21, 23, -20, 21])
                self.set_bb(HB.BOTTOM, [21, 25, 21, -23])
                self.set_bb(HB.RIGHT, [-20, 23, 21, 21])
                self.set_bb(HB.TOP, [20, 0, 20, 24])

            # Die A
            elif self.action == ACTION.DIE_A:
                pass

            # Die B
            elif self.action == ACTION.DIE_B:
                pass

            else:
                print("Invalid action: %s" % (str(self.action)))
                exit(-1)

        # Boo
        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.BOO):

            # Idle right
            if self.action == "stay" and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            # Idle left
            elif self.action == "stay" and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            # Fly right
            elif self.action == "fly" and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True

            # Fly left
            elif self.action == "fly" and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True

            # Die right
            elif self.action == "die" and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 1
                self.loop_animation = False

            # Die left
            elif self.action == "die" and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 1, 1
                self.loop_animation = False
            else:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 7
                self.loop_animation = False

        # Piranha plant
        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.PIRANHA_PLANT):

            # Pop
            if self.action == "pop":
                self.frame_count, self.frame_begin = 78, 0
                self.l, self.b, self.w, self.h = 50, 100 * 4, 50, 50
                self.loop_animation = False

        # Tile sets
        elif self.type_name == TN.TILESETS:
            if len(self.bounding_box) == 0:
                self.bounding_box[HB.BODY] = BoundingBox(HB.BODY)
                self.bounding_box[HB.LEFT] = BoundingBox(HB.LEFT)
                self.bounding_box[HB.BOTTOM] = BoundingBox(HB.BOTTOM)
                self.bounding_box[HB.RIGHT] = BoundingBox(HB.RIGHT)
                self.bounding_box[HB.TOP] = BoundingBox(HB.TOP)

            if (self.type_id == TID.CASTLE_BLOCK_50X50 or
                self.type_id == TID.BREAKABLE_BRICK or
                self.type_id == TID.EMPTY_BOX or
                self.type_id == TID.RANDOM_BOX
            ):
                self.set_bb(HB.BODY, [25, 25, 25, 25])
                self.set_bb(HB.LEFT, [25, 25, -20, 25])
                self.set_bb(HB.BOTTOM, [24, 25, 24, -20])
                self.set_bb(HB.RIGHT, [-20, 25, 25, 25])
                self.set_bb(HB.TOP, [24, -20, 24, 25])
            elif self.type_id == TID.CASTLE_BLOCK_50X100:
                self.set_bb(HB.BODY, [25, 50, 25, 50])
                self.set_bb(HB.LEFT, [25, 50, -20, 50])
                self.set_bb(HB.BOTTOM, [24, 50, 24, -45])
                self.set_bb(HB.RIGHT, [-20, 50, 25, 50])
                self.set_bb(HB.TOP, [24, -45, 24, 50])
            elif self.type_id == TID.CASTLE_BLOCK_100X50:
                self.set_bb(HB.BODY, [50, 25, 50, 25])
                self.set_bb(HB.LEFT, [50, 25, -45, 25])
                self.set_bb(HB.BOTTOM, [49, 25, 49, -20])
                self.set_bb(HB.RIGHT, [-45, 25, 50, 25])
                self.set_bb(HB.TOP, [49, -20, 49, 25])
            elif self.type_id == TID.CASTLE_BLOCK_100X100:
                self.set_bb(HB.BODY, [50, 50, 50, 50])
                self.set_bb(HB.LEFT, [50, 50, -45, 50])
                self.set_bb(HB.BOTTOM, [49, 50, 49, -45])
                self.set_bb(HB.RIGHT, [-45, 50, 50, 50])
                self.set_bb(HB.TOP, [49, -45, 49, 50])

        # Items
        elif self.type_name == TN.ITEMS:
            if len(self.bounding_box) == 0:
                self.bounding_box[HB.BODY] = BoundingBox(HB.BODY)
                self.bounding_box[HB.LEFT] = BoundingBox(HB.LEFT)
                self.bounding_box[HB.BOTTOM] = BoundingBox(HB.BOTTOM)
                self.bounding_box[HB.RIGHT] = BoundingBox(HB.RIGHT)
                self.bounding_box[HB.TOP] = BoundingBox(HB.TOP)
            self.switch_bb_all()

            if self.type_id == TID.SUPER_MUSHROOM:
                self.set_bb(HB.BODY, [24, 24, 24, 24])
                self.set_bb(HB.LEFT, [25, 25, -20, 25])
                self.set_bb(HB.BOTTOM, [24, 25, 24, -20])
                self.set_bb(HB.RIGHT, [-20, 25, 25, 25])
                self.set_bb(HB.TOP, [24, -20, 24, 25])

            elif self.type_id == TID.COIN:
                self.set_bb(HB.BODY, [25, 25, 25, 25])

        # Interactives
        elif self.type_name == TN.INTERACTIVES:
            if self.type_id == TID.WIRE_MESH:
                if len(self.bounding_box) == 0:
                    self.bounding_box[HB.BODY] = BoundingBox(HB.BODY)
                self.switch_bb_all()

                self: ob_interactive.WireMesh
                self.set_bb(HB.BODY, [
                    0, 0,
                    (self.index_x - 1) * ob_map.TILE_WIDTH,
                    (self.index_y - 1) * ob_map.TILE_HEIGHT
                ])

        else:
            print("Invalid type: %s / %s" % (str(self.type_name), str(self.type_id)))
            exit(-1)

    def set_clip(self, a=None):
        if a == self.action:
            return

        if a is not None:
            self.action = a

        # print("facing in set_info(): " + str(self.facing))

        # Mario_small
        if (self.type_name, self.type_id) == (TN.PLAYER, TID.MARIO_SMALL):

            # Idle right
            if self.action == ACTION.IDLE and self.facing == DIR.RIGHT:
                self.set_tpa(1.2)
                self.l, self.b, self.w, self.h = 50, 50 * 9, 50, 50
                self.frame_count, self.frame_begin = 27, 0
                self.loop_animation = True

            # Idle left
            elif self.action == ACTION.IDLE and self.facing == DIR.LEFT:
                self.set_tpa(1.2)
                self.l, self.b, self.w, self.h = 50, 50 * 8, 50, 50
                self.frame_count, self.frame_begin = 27, 0
                self.loop_animation = True

            # Walk right
            elif self.action == ACTION.WALK and self.facing == DIR.RIGHT:
                self.set_tpa(1.0)
                self.l, self.b, self.w, self.h = 50, 50 * 7, 50, 50
                self.frame_count, self.frame_begin = 18, 0
                self.loop_animation = True

            # Walk left
            elif self.action == ACTION.WALK and self.facing == DIR.LEFT:
                self.set_tpa(1.0)
                self.l, self.b, self.w, self.h = 50, 50 * 6, 50, 50
                self.frame_count, self.frame_begin = 18, 0
                self.loop_animation = True

            # Run right
            elif self.action == ACTION.RUN and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True

            # Run left
            elif self.action == ACTION.RUN and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 4, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True

            # Break right
            elif self.action == ACTION.BREAK and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 4, 50, 50
                self.frame_count, self.frame_begin = 1, 8
                self.loop_animation = False

            # Break left
            elif self.action == ACTION.BREAK and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 1, 8
                self.loop_animation = False

            # Swim right
            elif self.action == ACTION.SWIM and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 9, 0
                self.loop_animation = True

            # Swim left
            elif self.action == ACTION.SWIM and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 9, 0
                self.loop_animation = True

            # Hang
            elif self.action == ACTION.HANG:
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 6, 0
                self.loop_animation = True

            # Climb
            elif self.action == ACTION.CLIMB:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 14, 0
                self.loop_animation = True

            # Jump right
            elif self.action == ACTION.JUMP and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 7, 50, 50
                self.frame_count, self.frame_begin = 1, 18
                self.loop_animation = False

            # Jump left
            elif self.action == ACTION.JUMP and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 6, 50, 50
                self.frame_count, self.frame_begin = 1, 18
                self.loop_animation = False

            # Fall right
            elif self.action == ACTION.FALL and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 7, 50, 50
                self.frame_count, self.frame_begin = 1, 19
                self.loop_animation = False

            # Fall left
            elif self.action == ACTION.FALL and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 6, 50, 50
                self.frame_count, self.frame_begin = 1, 19
                self.loop_animation = False

            # Die A
            elif self.action == ACTION.DIE_A:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 1, 14
                self.loop_animation = False

            elif self.action == ACTION.SIT:
                pass

            else:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 1, 26
                self.loop_animation = False
                print("Invalid action: %s" % (str(self.action)))

        # Mario super
        elif (self.type_name, self.type_id) == (TN.PLAYER, TID.MARIO_SUPER):

            # Idle right
            if self.action == ACTION.IDLE and self.facing == DIR.RIGHT:
                self.set_tpa(1.2)
                self.l, self.b, self.w, self.h = 50, 100 * 9, 50, 100
                self.frame_count, self.frame_begin = 27, 0
                self.loop_animation = True

            # Idle left
            elif self.action == ACTION.IDLE and self.facing == DIR.LEFT:
                self.set_tpa(1.2)
                self.l, self.b, self.w, self.h = 50, 100 * 8, 50, 100
                self.frame_count, self.frame_begin = 27, 0
                self.loop_animation = True

            # Walk right
            elif self.action == ACTION.WALK and self.facing == DIR.RIGHT:
                self.set_tpa(0.8)
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 18, 0
                self.loop_animation = True

            # Walk left
            elif self.action == ACTION.WALK and self.facing == DIR.LEFT:
                self.set_tpa(0.8)
                self.l, self.b, self.w, self.h = 50, 100 * 6, 50, 100
                self.frame_count, self.frame_begin = 18, 0
                self.loop_animation = True

            # Run right
            elif self.action == ACTION.RUN and self.facing == DIR.RIGHT:
                self.set_tpa(0.5)
                self.l, self.b, self.w, self.h = 100, 100 * 5, 100, 100
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True

            # Run left
            elif self.action == ACTION.RUN and self.facing == DIR.LEFT:
                self.set_tpa(0.5)
                self.l, self.b, self.w, self.h = 100, 100 * 4, 100, 100
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True

            # Break right
            elif self.action == ACTION.BREAK and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 4, 100, 100
                self.frame_count, self.frame_begin = 1, 8
                self.loop_animation = False

            # Break left
            elif self.action == ACTION.BREAK and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 5, 100, 100
                self.frame_count, self.frame_begin = 1, 8
                self.loop_animation = False

            # Swim right
            elif self.action == ACTION.SWIM and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 3, 100, 100
                self.frame_count, self.frame_begin = 9, 0
                self.loop_animation = True

            # Swim left
            elif self.action == ACTION.SWIM and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 2, 100, 100
                self.frame_count, self.frame_begin = 9, 0
                self.loop_animation = True

            # Hang
            elif self.action == ACTION.HANG:
                self.l, self.b, self.w, self.h = 50, 100 * 1, 50, 100
                self.frame_count, self.frame_begin = 6, 0
                self.loop_animation = True

            # Climb
            elif self.action == ACTION.CLIMB:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 14, 0
                self.loop_animation = True

            # Sit right
            elif self.action == ACTION.SIT and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 9, 50, 100
                self.frame_count, self.frame_begin = 1, 27
                self.loop_animation = False

            # Sit left
            elif self.action == ACTION.SIT and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 8, 50, 100
                self.frame_count, self.frame_begin = 1, 27
                self.loop_animation = False

            # Jump right
            elif self.action == ACTION.JUMP and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 7, 100, 100
                self.frame_count, self.frame_begin = 1, 18 // 2
                self.loop_animation = False

            # Jump left
            elif self.action == ACTION.JUMP and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 6, 100, 100
                self.frame_count, self.frame_begin = 1, 18 // 2
                self.loop_animation = False

            # Fall right
            elif self.action == ACTION.FALL and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 7, 100, 100
                self.frame_count, self.frame_begin = 1, 20 // 2
                self.loop_animation = False

            # Fall left
            elif self.action == ACTION.FALL and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 6, 100, 100
                self.frame_count, self.frame_begin = 1, 20 // 2
                self.loop_animation = False

            else:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 1, 29
                self.loop_animation = False
                print("Invalid action: %s" % (str(self.action)))

        # Dry bones
        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.DRY_BONES):

            # Idle right
            if self.action == ACTION.IDLE and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            # Idle left
            elif self.action == ACTION.IDLE and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 6, 50, 100
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            # Walk right
            elif self.action == ACTION.WALK and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 5, 50, 100
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True

            # Walk left
            elif self.action == ACTION.WALK and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 4, 50, 100
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True

            # Break right
            elif self.action == ACTION.BREAK and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 3, 50, 100
                self.frame_count, self.frame_begin = 12, 0
                self.loop_animation = False

            # Break left
            elif self.action == ACTION.BREAK and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 2, 50, 100
                self.frame_count, self.frame_begin = 12, 0
                self.loop_animation = False

            # Restore right
            elif self.action == ACTION.RESTORE and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 1, 50, 100
                self.frame_count, self.frame_begin = 15, 0
                self.loop_animation = False

            # Restore left
            elif self.action == ACTION.RESTORE and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 15, 0
                self.loop_animation = False

            else:
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 1, 15
                self.loop_animation = False
                print("Invalid action: %s" % (str(self.action)))

        # Goomba
        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.GOOMBA):

            # Idle right
            if self.action == ACTION.IDLE and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            # Idle left
            elif self.action == ACTION.IDLE and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 4, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            # Walk right
            elif self.action == ACTION.WALK and self.facing == DIR.RIGHT:
                self.set_tpa(1.0)
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True

            # Walk left
            elif self.action == ACTION.WALK and self.facing == DIR.LEFT:
                self.set_tpa(1.0)
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True

            # Die A
            elif self.action == ACTION.DIE_A:
                self.set_tpa(0.2)
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 3, 0
                self.loop_animation = False

            # Die B
            elif self.action == ACTION.DIE_B:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            else:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 1, 15
                self.loop_animation = False
                print("Invalid action: %s" % (str(self.action)))

        # Boo
        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.BOO):

            # Idle right
            if self.action == ACTION.IDLE and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            # Idle left
            elif self.action == ACTION.IDLE and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False

            # Fly right
            elif self.action == ACTION.FLY and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True

            # Fly left
            elif self.action == ACTION.FLY and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True

            # Die right
            elif self.action == ACTION.DIE_A and self.facing == DIR.RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 1
                self.loop_animation = False

            # Die left
            elif self.action == ACTION.DIE_B and self.facing == DIR.LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 1, 1
                self.loop_animation = False

            else:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 7
                self.loop_animation = False
                print("Invalid action: %s" % (str(self.action)))

        # Piranha plant
        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.PIRANHA_PLANT):

            # Pop
            if self.action == ACTION.ATTACK:
                self.frame_count, self.frame_begin = 78, 0
                self.l, self.b, self.w, self.h = 50, 100 * 4, 50, 50
                self.loop_animation = False

        # Items
        elif self.type_name == TN.ITEMS:
            if self.type_id == TID.COIN:
                self.set_tpa(0.5)
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 4, 0
                self.loop_animation = True

        # Tile sets
        elif self.type_name == TN.TILESETS:
            if self.type_id == TID.RANDOM_BOX:
                self.set_tpa(0.8)
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 4, 0
                self.loop_animation = True

            elif self.type_id == TID.BREAKABLE_BRICK:
                self.set_tpa(0.8)
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 4, 0
                self.loop_animation = True

        # Interactives
        elif self.type_name == TN.INTERACTIVES:
            if self.type_id == TID.WIRE_MESH:
                if self.action == ACTION.PIECE_LT:
                    self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                    self.frame_count, self.frame_begin = 1, 0
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_T:
                    self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                    self.frame_count, self.frame_begin = 1, 1
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_RT:
                    self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                    self.frame_count, self.frame_begin = 1, 2
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_L:
                    self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                    self.frame_count, self.frame_begin = 1, 0
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_M:
                    self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                    self.frame_count, self.frame_begin = 1, 1
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_R:
                    self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                    self.frame_count, self.frame_begin = 1, 2
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_LB:
                    self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                    self.frame_count, self.frame_begin = 1, 0
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_B:
                    self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                    self.frame_count, self.frame_begin = 1, 1
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_RB:
                    self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                    self.frame_count, self.frame_begin = 1, 2
                    self.loop_animation = False


        # Foreground exclusives
        elif self.type_name == TN.FOREGROUND:
            self: ob_foreground.Foreground
            if self.pm_type_id == TID.BRICK_PIECE:
                if self.action == ACTION.PIECE_LT:
                    self.l, self.b, self.w, self.h = 25, 25 * 1, 25, 25
                    self.frame_count, self.frame_begin = 1, 0
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_RT:
                    self.l, self.b, self.w, self.h = 25, 25 * 1, 25, 25
                    self.frame_count, self.frame_begin = 1, 1
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_LB:
                    self.l, self.b, self.w, self.h = 25, 25 * 0, 25, 25
                    self.frame_count, self.frame_begin = 1, 0
                    self.loop_animation = False
                elif self.action == ACTION.PIECE_RB:
                    self.l, self.b, self.w, self.h = 25, 25 * 0, 25, 25
                    self.frame_count, self.frame_begin = 1, 1
                    self.loop_animation = False


        self.frame = self.frame_begin

    def set_info(self, a=None):
        self.set_clip(a)
        self.init_bb()
        self.set_bb_size()

def test_object():
    open_canvas()

    object = GameObject()

    close_canvas()


if __name__ == "__main__":
    test_object()
