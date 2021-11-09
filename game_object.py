from pico2d import *
from value import *
from abc import *
from hit_box import *

CO_NONE = 0
CO_MARIO_SMALL = 1
CO_MARIO_SUPER = 2
CO_DRY_BONES = 3
CO_GOOMBA = 4
CO_BOO = 5
CO_PIRANHA_PLANT = 6

D_NONE = 0
D_RIGHT = 1
D_LEFT = -1

IMAGE_LOCATION = [
    'resource\\no_image.png',
    'resource\\characters\\mario_small.png', 'resource\\characters\\mario_super.png',
    'resource\\characters\\dry_bones.png', 'resource\\characters\\goomba.png',
    'resource\\characters\\boo.png', 'resource\\characters\\piranha_plant.png'
]

SPRITES_MARIO_SUPER = [
    "stay", "walk", "run", "swim",
    "hang", "climb", "jump_up", "jump_down"
                                "crawl"
]

SPRITES_MARIO_SMALL = [
    "stay", "walk", "run", "swim",
    "hang", "climb", "jump_up", "jump_down"
                                "die"
]

SPRITES_WARURU = [
    "stay", "walk", "break", "restore"
]

SPRITES_GOOMBA = [
    "stay", "walk", "dieA", "dieB"
]

SPRITES_BOO = [
    "stay", "fly", "die"
]

SPRITES_PIRANHA_PLANT = [
    "pop"
]

IMAGE_SPRITES = [
    ["none"],
    SPRITES_MARIO_SMALL,
    SPRITES_MARIO_SUPER,
    SPRITES_WARURU,
    SPRITES_GOOMBA,
    SPRITES_BOO,
    SPRITES_PIRANHA_PLANT
]


class Object:
    image_inst = None
    image = {}

    def __init__(self, type_name, type_id):

        # Image initialization
        if None == Object.image_inst:
            Object.image_inst = (
                load_image('resource\\characters\\mario_small.png'),
                load_image('resource\\characters\\mario_super.png'),
                load_image('resource\\tileset\\block50x50.png'),
                load_image('resource\\tileset\\block50x100.png'),
                load_image('resource\\tileset\\block100x50.png'),
                load_image('resource\\tileset\\block100x100.png'),
                load_image('resource\\characters\\goomba.png'),
                load_image('resource\\characters\\dry_bones.png'),
                load_image('resource\\characters\\boo.png'),
                load_image('resource\\characters\\piranha_plant.png'),
                load_image('resource\\characters\\spinning_spike.png'),
                load_image('resource\\items\\coin.png'),
                load_image('resource\\items\\fire_flower.png'),
                load_image('resource\\items\\life_mushroom.png'),
                load_image('resource\\items\\starcoin.png'),
                load_image('resource\\items\\super_mushroom.png'),
                load_image('resource\\items\\super_star.png')
            )

            Object.image = {
                (TN.PLAYER, TID.MARIO_SMALL): Object.image_inst[nbr(begin=True)],
                (TN.PLAYER, TID.MARIO_SUPER): Object.image_inst[nbr()],
                (TN.TILESETS, TID.CASTLE_BLOCK_50X50): Object.image_inst[nbr()],
                (TN.TILESETS, TID.CASTLE_BLOCK_50X100): Object.image_inst[nbr()],
                (TN.TILESETS, TID.CASTLE_BLOCK_100X50): Object.image_inst[nbr()],
                (TN.TILESETS, TID.CASTLE_BLOCK_100X100): Object.image_inst[nbr()],
                (TN.ENEMIES, TID.GOOMBA): Object.image_inst[nbr()],
                (TN.ENEMIES, TID.DRY_BONES): Object.image_inst[nbr()],
                (TN.ENEMIES, TID.BOO): Object.image_inst[nbr()],
                (TN.ENEMIES, TID.PIRANHA_PLANT): Object.image_inst[nbr()],
                (TN.ENEMIES, TID.SPINNING_SPIKE): Object.image_inst[nbr()],
                (TN.ITEMS, TID.COIN): Object.image_inst[nbr()],
                (TN.ITEMS, TID.FIRE_FLOWER): Object.image_inst[nbr()],
                (TN.ITEMS, TID.LIFE_MUSHROOM): Object.image_inst[nbr()],
                (TN.ITEMS, TID.STAR_COIN): Object.image_inst[nbr()],
                (TN.ITEMS, TID.SUPER_MUSHROOM): Object.image_inst[nbr()],
                (TN.ITEMS, TID.super_star): Object.image_inst[nbr()],
            }

        # Object location point
        self.x, self.y = 0, 0

        self.px, self.py = self.x, self.y

        # Hit Box
        self.hit_boxes = [HitBox(self.x, self.y) for i in range(4)]

        # Object moving value
        self.speed = 0

        # Animation sprite value
        self.l, self.b, self.w, self.h = 0, 0, 0, 0

        # Animation Direction
        self.direction = D_RIGHT
        self.prev_direction = self.direction

        # Object Type
        self.type_name = type_name
        self.type_id = type_id

        # Object action with sprite animation
        self.action = ""

        # Animation frame value
        self.frames = 0
        self.frame_begin = 0
        self.frame_count = 0

        # Animation control value
        self.loop_animation = False

    def draw(self):
        Object.image[(self.type_name, self.type_id)].draw(self.x, self.y)

    def clip_draw(self):
        if self.frame_count == 1:
            self.frames = 0

        Object.image[(self.type_name, self.type_id)].clip_draw(
            (self.frames + self.frame_begin) * self.l, self.b,
            self.w, self.h, self.x, self.y)

    @abstractmethod
    def update(self):
        pass

    def update_frame(self):
        if self.frame_count == 0:
            self.frame_count = 1
            print("count value error")

        if self.frame_count == 1:
            return

        if not self.loop_animation:
            if self.frames + 1 == self.frame_count:
                return

        self.frames = (self.frames + 1) % self.frame_count

    def set_clip(self, a=""):
        if a == self.action and self.prev_direction == self.direction:
            return

        self.prev_direction = self.direction

        if a != "":
            self.action = a

        if (self.type_name, self.type_id) == (TN.PLAYER, TID.MARIO_SMALL):
            self.correction_y = 15
            self.hit_boxes[HB.COLLISION].set_info(NAME.PLAYER_SMALL, TYPE.HIT)
            self.hit_boxes[HB.STAND].set_info(NAME.PLAYER_SMALL, TYPE.STAND)
            self.hit_boxes[HB.ATTACK].set_info(NAME.PLAYER_SMALL, TYPE.ATTACK)
            self.hit_boxes[HB.BREAK].set_info(NAME.PLAYER_SMALL, TYPE.BREAK)

            if self.action == "stay" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 9, 50, 50
                self.frame_count, self.frame_begin = 27, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 13, 13)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 12, 12)
                self.loop_animation = True
            elif self.action == "stay" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 8, 50, 50
                self.frame_count, self.frame_begin = 27, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 13, 13)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 12, 12)
                self.loop_animation = True
            elif self.action == "walk" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 7, 50, 50
                self.frame_count, self.frame_begin = 18, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 13, 13)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 12, 12)
                self.loop_animation = True
            elif self.action == "walk" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 6, 50, 50
                self.frame_count, self.frame_begin = 18, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 13, 13)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 12, 12)
                self.loop_animation = True
            elif self.action == "run" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 13, 20)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 12, 18)
                self.loop_animation = True
            elif self.action == "run" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 4, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 20, 13)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 18, 12)
                self.loop_animation = True
            elif self.action == "swim" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 9, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 13, 20)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 12, 18)
                self.loop_animation = True
            elif self.action == "swim" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 9, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 20, 13)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 18, 12)
                self.loop_animation = True
            elif self.action == "hang":
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 6, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = False
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 13, 13)
                self.loop_animation = True
            elif self.action == "climb":
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 14, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 13, 13)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 12, 12)
                self.loop_animation = True
            elif self.action == "jump_up" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 7, 50, 50
                self.frame_count, self.frame_begin = 1, 18
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = False
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = True
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 13, 12)
                self.hit_boxes[HB.BREAK].set_range(25, -23, 12, 8)
                self.loop_animation = False
            elif self.action == "jump_down" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 7, 50, 50
                self.frame_count, self.frame_begin = 1, 19
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = True
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 12, 12)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 11, 11)
                self.hit_boxes[HB.ATTACK].set_range(-8, 15, 8, 16)
                self.loop_animation = False
            elif self.action == "jump_up" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 6, 50, 50
                self.frame_count, self.frame_begin = 1, 18
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = False
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = True
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 12, 13)
                self.hit_boxes[HB.BREAK].set_range(25, -23, 8, 12)
                self.loop_animation = False
            elif self.action == "jump_down" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 6, 50, 50
                self.frame_count, self.frame_begin = 1, 19
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = True
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(22, 15, 12, 12)
                self.hit_boxes[HB.STAND].set_range(-14, 15, 11, 11)
                self.hit_boxes[HB.ATTACK].set_range(-8, 15, 16, 8)
                self.loop_animation = False
            elif self.action == "die":
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 1, 14
                self.hit_boxes[HB.COLLISION].is_on = False
                self.hit_boxes[HB.STAND].is_on = False
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.loop_animation = False

            else:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 1, 26
                self.loop_animation = False

        elif (self.type_name, self.type_id) == (TN.PLAYER, TID.MARIO_SUPER):
            self.correction_y = 40
            self.hit_boxes[HB.COLLISION].set_info(NAME.PLAYER_SUPER, TYPE.HIT)
            self.hit_boxes[HB.STAND].set_info(NAME.PLAYER_SUPER, TYPE.STAND)
            self.hit_boxes[HB.ATTACK].set_info(NAME.PLAYER_SUPER, TYPE.ATTACK)
            self.hit_boxes[HB.BREAK].set_info(NAME.PLAYER_SUPER, TYPE.BREAK)

            if self.action == "stay" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 9, 50, 100
                self.frame_count, self.frame_begin = 27, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(30, 40, 15, 15)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 14, 14)
                self.loop_animation = True
            elif self.action == "stay" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 8, 50, 100
                self.frame_count, self.frame_begin = 27, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(30, 40, 15, 15)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 14, 14)
                self.loop_animation = True
            elif self.action == "walk" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 18, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(30, 40, 15, 15)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 14, 14)
                self.loop_animation = True
            elif self.action == "walk" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 6, 50, 100
                self.frame_count, self.frame_begin = 18, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(30, 40, 15, 15)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 14, 14)
                self.loop_animation = True
            elif self.action == "run" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 5, 100, 100
                self.frame_count, self.frame_begin = 8, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(20, 40, 25, 25)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 24, 24)
                self.loop_animation = True
            elif self.action == "run" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 4, 100, 100
                self.frame_count, self.frame_begin = 8, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(20, 40, 25, 25)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 24, 24)
                self.loop_animation = True
            elif self.action == "swim" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 3, 100, 100
                self.frame_count, self.frame_begin = 9, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(21, 40, 25, 28)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 24, 27)
                self.loop_animation = True
            elif self.action == "swim" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 2, 100, 100
                self.frame_count, self.frame_begin = 9, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(21, 40, 28, 25)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 27, 24)
                self.loop_animation = True
            elif self.action == "hang":
                self.l, self.b, self.w, self.h = 50, 100 * 1, 50, 100
                self.frame_count, self.frame_begin = 6, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = False
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(30, 40, 15, 15)
                self.loop_animation = True
            elif self.action == "climb":
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 14, 0
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(30, 40, 15, 15)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 14, 14)
                self.loop_animation = True
            elif self.action == "crawl" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 9, 50, 100
                self.frame_count, self.frame_begin = 1, 27
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(-7, 40, 15, 15)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 14, 14)
                self.loop_animation = False
            elif self.action == "crawl" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 8, 50, 100
                self.frame_count, self.frame_begin = 1, 27
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(-7, 40, 15, 15)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 14, 14)
                self.loop_animation = False
            elif self.action == "jump_up" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 7, 100, 100
                self.frame_count, self.frame_begin = 1, 18 // 2
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = False
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = True
                self.hit_boxes[HB.COLLISION].set_range(30, 36, 15, 15)
                self.hit_boxes[HB.BREAK].set_range(34, -30, 15, 15)
                self.loop_animation = False
            elif self.action == "jump_down" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 7, 100, 100
                self.frame_count, self.frame_begin = 1, 20 // 2
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = True
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(30, 40, 15, 15)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 14, 14)
                self.hit_boxes[HB.ATTACK].set_range(-32, 41, 12, 28)
                self.loop_animation = False
            elif self.action == "jump_up" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 6, 100, 100
                self.frame_count, self.frame_begin = 1, 18 // 2
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = False
                self.hit_boxes[HB.ATTACK].is_on = False
                self.hit_boxes[HB.BREAK].is_on = True
                self.hit_boxes[HB.COLLISION].set_range(30, 36, 15, 15)
                self.hit_boxes[HB.BREAK].set_range(34, -30, 15, 15)
                self.loop_animation = False
            elif self.action == "jump_down" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 6, 100, 100
                self.frame_count, self.frame_begin = 1, 20 // 2
                self.hit_boxes[HB.COLLISION].is_on = True
                self.hit_boxes[HB.STAND].is_on = True
                self.hit_boxes[HB.ATTACK].is_on = True
                self.hit_boxes[HB.BREAK].is_on = False
                self.hit_boxes[HB.COLLISION].set_range(30, 40, 15, 15)
                self.hit_boxes[HB.STAND].set_range(-39, 40, 14, 14)
                self.hit_boxes[HB.ATTACK].set_range(-32, 41, 28, 12)
                self.loop_animation = False

            else:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 1, 29
                self.loop_animation = False

        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.DRY_BONES):
            self.correction_y = 40

            if self.action == "stay" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "stay" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 6, 50, 100
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "walk" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 5, 50, 100
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True
            elif self.action == "walk" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 4, 50, 100
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True
            elif self.action == "break" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 3, 50, 100
                self.frame_count, self.frame_begin = 12, 0
                self.loop_animation = False
            elif self.action == "break" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 2, 50, 100
                self.frame_count, self.frame_begin = 12, 0
                self.loop_animation = False
            elif self.action == "restore" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 1, 50, 100
                self.frame_count, self.frame_begin = 15, 0
                self.loop_animation = False
            elif self.action == "restore" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 15, 0
                self.loop_animation = False
            else:
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 1, 15
                self.loop_animation = False

        elif (self.type_name, self.type_id) == (TN.ENEMIES, TID.GOOMBA):
            self.correction_y = 15

            if self.action == "stay" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "stay" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 4, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "walk" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 16, 0
                self.loop_animation = True
            elif self.action == "walk" and self.direction == D_LEFT:
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
            self.correction_y = 25
            if self.action == "stay" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "stay" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.loop_animation = False
            elif self.action == "fly" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True
            elif self.action == "fly" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.loop_animation = True
            elif self.action == "die" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 1
                self.loop_animation = False
            elif self.action == "die" and self.direction == D_LEFT:
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

        self.frames = self.frame_begin
