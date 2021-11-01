from pico2d import *
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
    'resource\\characters\\mario_small.png',  'resource\\characters\\mario_super.png',
    'resource\\characters\\dry_bones.png',    'resource\\characters\\goomba.png',
    'resource\\characters\\boo.png',          'resource\\characters\\piranha_plant.png'
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

class Character_Object:
    def __init__( self ):

        # Object location point
        self.x, self.y = 0, 0
        self.wx, self.wy = 0, 0
        self.correction_y = 0

        self.px, self.py = self.x, self.y

        # Hit Box
        self.hit_box = HitBox(self.x, self.y, img_id = 2)
        self.stand_box = HitBox(self.x, self.y, img_id = 2)
        self.attack_box = HitBox(self.x, self.y, on=False, img_id = 0)
        self.break_box = HitBox(self.x, self.y, on=False, img_id = 1)

        # Object moving value
        self.speed = 0

        # Animation sprite value
        self.l, self.b, self.w, self.h = 0, 0, 0, 0

        # Animation Direction
        self.direction = D_RIGHT
        self.prev_direction = self.direction

        # Sprite image
        self.image_id = CO_NONE
        self.image = load_image( IMAGE_LOCATION[self.image_id ] )

        # Object action with sprite animation
        self.action = ""

        # Animation frame value
        self.frames = 0
        self.frame_begin = 0
        self.frame_count = 0

        # Animation control value
        self.loop_animation = False

    def init_decode(self, mx, my):
        self.wx = mx * 50 / 2
        self.wy = my * 50 / 2

    def draw( self ):
        self.image.draw(self.x, self.y)

    def clip_draw( self ):
        if self.frame_count == 1:
            self.frames = 0

        self.image.clip_draw((self.frames + self.frame_begin) * self.l, self.b,
                             self.w, self.h, self.x, self.y)

    def update_frame( self ):
        if self.frame_count == 0:
            self.frame_count = 1
            print("count value error")

        if self.frame_count == 1:
            return

        if not self.loop_animation:
            if self.frames + 1 == self.frame_count:
                return

        self.frames = (self.frames + 1) % self.frame_count

    def set_clip( self , a = ""):
        if a == self.action and self.prev_direction == self.direction:
            return

        self.prev_direction = self.direction

        if a != "":
            self.action = a

        self.image = load_image( IMAGE_LOCATION[self.image_id] )

        if self.image_id == CO_MARIO_SMALL:
            self.correction_y = 15
            self.hit_box.set_info(NAME.PLAYER_SMALL, TYPE.HIT)
            self.stand_box.set_info(NAME.PLAYER_SMALL, TYPE.STAND)
            self.attack_box.set_info(NAME.PLAYER_SMALL, TYPE.ATTACK)
            self.break_box.set_info(NAME.PLAYER_SMALL, TYPE.BREAK)

            if self.action == "stay" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50*9, 50, 50
                self.frame_count, self.frame_begin = 27, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 13, 13)
                self.stand_box.set_range(-14, 15, 12, 12)
                self.loop_animation = True
            elif self.action == "stay" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50*8, 50, 50
                self.frame_count, self.frame_begin = 27, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 13, 13)
                self.stand_box.set_range(-14, 15, 12, 12)
                self.loop_animation = True
            elif self.action == "walk" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50*7, 50, 50
                self.frame_count, self.frame_begin = 18, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 13, 13)
                self.stand_box.set_range(-14, 15, 12, 12)
                self.loop_animation = True
            elif self.action == "walk" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50*6, 50, 50
                self.frame_count, self.frame_begin = 18, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 13, 13)
                self.stand_box.set_range(-14, 15, 12, 12)
                self.loop_animation = True
            elif self.action == "run" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50*5, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 13, 20)
                self.stand_box.set_range(-14, 15, 12, 18)
                self.loop_animation = True
            elif self.action == "run" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50*4, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 20, 13)
                self.stand_box.set_range(-14, 15, 18, 12)
                self.loop_animation = True
            elif self.action == "swim" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50*3, 50, 50
                self.frame_count, self.frame_begin = 9, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 13, 20)
                self.stand_box.set_range(-14, 15, 12, 18)
                self.loop_animation = True
            elif self.action == "swim" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50*2, 50, 50
                self.frame_count, self.frame_begin = 9, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 20, 13)
                self.stand_box.set_range(-14, 15, 18, 12)
                self.loop_animation = True
            elif self.action == "hang":
                self.l, self.b, self.w, self.h = 50, 50*1, 50, 50
                self.frame_count, self.frame_begin = 6, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = False
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 13, 13)
                self.loop_animation = True
            elif self.action == "climb":
                self.l, self.b, self.w, self.h = 50, 50*0, 50, 50
                self.frame_count, self.frame_begin = 14, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 13, 13)
                self.stand_box.set_range(-14, 15, 12, 12)
                self.loop_animation = True
            elif self.action == "jump_up" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50*7, 50, 50
                self.frame_count, self.frame_begin = 1, 18
                self.hit_box.is_on = True
                self.stand_box.is_on = False
                self.attack_box.is_on = False
                self.break_box.is_on = True
                self.hit_box.set_range(22, 15, 13, 12)
                self.break_box.set_range(25, -23, 12, 8)
                self.loop_animation = False
            elif self.action == "jump_down" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 50*7, 50, 50
                self.frame_count, self.frame_begin = 1, 19
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = True
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 12, 12)
                self.stand_box.set_range(-14, 15, 11, 11)
                self.attack_box.set_range(-8, 15, 8, 16)
                self.loop_animation = False
            elif self.action == "jump_up" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50*6, 50, 50
                self.frame_count, self.frame_begin = 1, 18
                self.hit_box.is_on = True
                self.stand_box.is_on = False
                self.attack_box.is_on = False
                self.break_box.is_on = True
                self.hit_box.set_range(22, 15, 12, 13)
                self.break_box.set_range(25, -23, 8, 12)
                self.loop_animation = False
            elif self.action == "jump_down" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 50*6, 50, 50
                self.frame_count, self.frame_begin = 1, 19
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = True
                self.break_box.is_on = False
                self.hit_box.set_range(22, 15, 12, 12)
                self.stand_box.set_range(-14, 15, 11, 11)
                self.attack_box.set_range(-8, 15, 16, 8)
                self.loop_animation = False
            elif self.action == "die":
                self.l, self.b, self.w, self.h = 50, 50*0, 50, 50
                self.frame_count, self.frame_begin = 1, 14
                self.hit_box.is_on = False
                self.stand_box.is_on = False
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.loop_animation = False

            else:
                self.l, self.b, self.w, self.h = 50, 50*0, 50, 50
                self.frame_count, self.frame_begin = 1, 26
                self.loop_animation = False

        elif self.image_id == CO_MARIO_SUPER:
            self.correction_y = 40
            self.hit_box.set_info(NAME.PLAYER_SUPER, TYPE.HIT)
            self.stand_box.set_info(NAME.PLAYER_SUPER, TYPE.STAND)
            self.attack_box.set_info(NAME.PLAYER_SUPER, TYPE.ATTACK)
            self.break_box.set_info(NAME.PLAYER_SUPER, TYPE.BREAK)

            if self.action == "stay" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 9, 50, 100
                self.frame_count, self.frame_begin = 27, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(30, 40, 15, 15)
                self.stand_box.set_range(-39, 40, 14, 14)
                self.loop_animation = True
            elif self.action == "stay" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 8, 50, 100
                self.frame_count, self.frame_begin = 27, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(30, 40, 15, 15)
                self.stand_box.set_range(-39, 40, 14, 14)
                self.loop_animation = True
            elif self.action == "walk" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 18, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(30, 40, 15, 15)
                self.stand_box.set_range(-39, 40, 14, 14)
                self.loop_animation = True
            elif self.action == "walk" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 6, 50, 100
                self.frame_count, self.frame_begin = 18, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(30, 40, 15, 15)
                self.stand_box.set_range(-39, 40, 14, 14)
                self.loop_animation = True
            elif self.action == "run" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 5, 100, 100
                self.frame_count, self.frame_begin = 8, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(20, 40, 25, 25)
                self.stand_box.set_range(-39, 40, 24, 24)
                self.loop_animation = True
            elif self.action == "run" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 4, 100, 100
                self.frame_count, self.frame_begin = 8, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(20, 40, 25, 25)
                self.stand_box.set_range(-39, 40, 24, 24)
                self.loop_animation = True
            elif self.action == "swim" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 3, 100, 100
                self.frame_count, self.frame_begin = 9, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(21, 40, 25, 28)
                self.stand_box.set_range(-39, 40, 24, 27)
                self.loop_animation = True
            elif self.action == "swim" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 2, 100, 100
                self.frame_count, self.frame_begin = 9, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(21, 40, 28, 25)
                self.stand_box.set_range(-39, 40, 27, 24)
                self.loop_animation = True
            elif self.action == "hang":
                self.l, self.b, self.w, self.h = 50, 100 * 1, 50, 100
                self.frame_count, self.frame_begin = 6, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = False
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(30, 40, 15, 15)
                self.loop_animation = True
            elif self.action == "climb":
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 14, 0
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(30, 40, 15, 15)
                self.stand_box.set_range(-39, 40, 14, 14)
                self.loop_animation = True
            elif self.action == "crawl" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 50, 100 * 9, 50, 100
                self.frame_count, self.frame_begin = 1, 27
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(-7, 40, 15, 15)
                self.stand_box.set_range(-39, 40, 14, 14)
                self.loop_animation = False
            elif self.action == "crawl" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 50, 100 * 8, 50, 100
                self.frame_count, self.frame_begin = 1, 27
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = False
                self.break_box.is_on = False
                self.hit_box.set_range(-7, 40, 15, 15)
                self.stand_box.set_range(-39, 40, 14, 14)
                self.loop_animation = False
            elif self.action == "jump_up" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 7, 100, 100
                self.frame_count, self.frame_begin = 1, 18//2
                self.hit_box.is_on = True
                self.stand_box.is_on = False
                self.attack_box.is_on = False
                self.break_box.is_on = True
                self.hit_box.set_range(30, 36, 15, 15)
                self.break_box.set_range(34, -30, 15, 15)
                self.loop_animation = False
            elif self.action == "jump_down" and self.direction == D_RIGHT:
                self.l, self.b, self.w, self.h = 100, 100 * 7, 100, 100
                self.frame_count, self.frame_begin = 1, 20//2
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = True
                self.break_box.is_on = False
                self.hit_box.set_range(30, 40, 15, 15)
                self.stand_box.set_range(-39, 40, 14, 14)
                self.attack_box.set_range(-32, 41, 12, 28)
                self.loop_animation = False
            elif self.action == "jump_up" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 6, 100, 100
                self.frame_count, self.frame_begin = 1, 18//2
                self.hit_box.is_on = True
                self.stand_box.is_on = False
                self.attack_box.is_on = False
                self.break_box.is_on = True
                self.hit_box.set_range(30, 36, 15, 15)
                self.break_box.set_range(34, -30, 15, 15)
                self.loop_animation = False
            elif self.action == "jump_down" and self.direction == D_LEFT:
                self.l, self.b, self.w, self.h = 100, 100 * 6, 100, 100
                self.frame_count, self.frame_begin = 1, 20//2
                self.hit_box.is_on = True
                self.stand_box.is_on = True
                self.attack_box.is_on = True
                self.break_box.is_on = False
                self.hit_box.set_range(30, 40, 15, 15)
                self.stand_box.set_range(-39, 40, 14, 14)
                self.attack_box.set_range(-32, 41, 28, 12)
                self.loop_animation = False

            else:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 1, 29
                self.loop_animation = False

        elif self.image_id == CO_DRY_BONES:
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

        elif self.image_id == CO_GOOMBA:
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

        elif self.image_id == CO_BOO:
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

        elif self.image_id == CO_PIRANHA_PLANT:
            if self.action == "pop":
                self.frame_count, self.frame_begin = 78, 0
                self.l, self.b, self.w, self.h = 50, 100 * 4, 50, 50
                self.loop_animation = False

        self.frames = self.frame_begin

