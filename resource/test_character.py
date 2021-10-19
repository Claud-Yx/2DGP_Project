from pico2d import *

PC_MARIO_SMALL = 0
PC_MARIO_SUPER = 1
PC_DRY_BONES = 2
PC_GOOMBA = 3
PC_BOO = 4
PC_PIRANHA_PLANT = 5

IMAGE_LOCATES = [
    'characters\\mario_small.png', 'characters\\mario_super.png',
    'characters\\dry_bones.png', 'characters\\goomba.png',
    'characters\\boo.png', 'characters\\piranha_plant.png'
]

SPRITES_MARIO_SUPER = [
    "stayR", "stayL", "walkR", "walkL", "runR", "runL", "swimR", "swimL",
    "hang", "climb", "jumpR_up", "jumpR_down", "jumpL_up", "jumpL_down",
    "crawlR", "crawlL"
]

SPRITES_MARIO_SMALL = [
    "stayR", "stayL", "walkR", "walkL", "runR", "runL", "swimR", "swimL",
    "hang", "climb", "jumpR_up", "jumpR_down", "jumpL_up", "jumpL_down",
    "die"
]

SPRITES_WARURU = [
    "stayR", "stayL", "walkR", "walkL", "breakR", "breakL", "restoreR", "restoreL"
]

SPRITES_GOOMBA = [
    "stayR", "stayL", "walkR", "walkL", "dieA", "dieB"
]

SPRITES_BOO = [
    "stayR", "stayL", "flyR", "flyL", "dieR", "dieL"
]

SPRITES_PIRANHA_PLANT = [
    "pop"
]

IMAGE_SPRITES = [
    SPRITES_MARIO_SMALL, SPRITES_MARIO_SUPER, SPRITES_WARURU, SPRITES_GOOMBA,
    SPRITES_BOO, SPRITES_PIRANHA_PLANT
]


class Test:

    def __init__(self):
        self.image_id = PC_MARIO_SMALL
        self.image_sprite_id = 0
        self.image = load_image(IMAGE_LOCATES[self.image_id])
        self.image_sprite = IMAGE_SPRITES[self.image_id][self.image_sprite_id]
        self.l, self.b, self.w, self.h = 0, 0, 0, 0
        self.frames = 0
        self.frame_count = 1
        self.frame_begin = 0
        self.clip_loop = True
        self.clip_stop = False
        self.set_clip()

    def clip_draw( self, x, y):
        if self.image_id == PC_PIRANHA_PLANT and self.image_sprite == "pop":
            newl = (self.frames % (self.frame_count // 3))
            newb = 100 * ((self.frame_count - (self.frames + 1)) // 26 + 1)
            self.image.clip_draw( newl * self.l, newb, self.w, self.h, x, y )
        else:
            self.image.clip_draw(self.frames * self.l, self.b, self.w, self.h, x, y)

    def frame_update( self ):
        if not self.clip_loop:
            self.clip_loop = True
            self.clip_stop = True

        if self.clip_stop:
            if self.frames == self.frame_count + self.frame_begin - 1:
                return

        self.frames = (self.frames + 1) % self.frame_count + self.frame_begin

    def frame_init( self ):
        self.frames = 0

    def handle_events(self):

        events = get_events()

        for event in events:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    return False
                elif event.key == SDLK_RIGHT:
                    self.image_sprite_id += 1
                    if len( IMAGE_SPRITES[self.image_id] ) <= self.image_sprite_id:
                        self.image_sprite_id = PC_MARIO_SMALL
                    self.set_clip()

                elif event.key == SDLK_LEFT:
                    self.image_sprite_id -= 1
                    if 0 > self.image_sprite_id:
                        self.image_sprite_id = len( IMAGE_SPRITES[self.image_id] ) - 1
                    self.set_clip()

                elif event.key == SDLK_UP:
                    self.image_sprite_id = 0
                    self.image_id += 1
                    if len( IMAGE_LOCATES ) <= self.image_id:
                        self.image_id = 0
                    self.set_clip()

                elif event.key == SDLK_DOWN:
                    self.image_sprite_id = 0
                    self.image_id -= 1
                    if 0 > self.image_id:
                        self.image_id = len( IMAGE_LOCATES ) - 1
                    self.set_clip()

            elif event.type == SDL_QUIT:
                return False

        return True

    def set_clip( self ):
        self.clip_stop = False
        self.image = load_image(IMAGE_LOCATES[self.image_id])
        self.image_sprite = IMAGE_SPRITES[self.image_id][self.image_sprite_id]

        if self.image_id == PC_MARIO_SMALL:
            if self.image_sprite == "stayR":
                self.l, self.b, self.w, self.h = 50, 50*9, 50, 50
                self.frame_count, self.frame_begin = 27, 0
                self.clip_loop = True
            elif self.image_sprite == "stayL":
                self.l, self.b, self.w, self.h = 50, 50*8, 50, 50
                self.frame_count, self.frame_begin = 27, 0
                self.clip_loop = True
            elif self.image_sprite == "walkR":
                self.l, self.b, self.w, self.h = 50, 50*7, 50, 50
                self.frame_count, self.frame_begin = 18, 0
                self.clip_loop = True
            elif self.image_sprite == "walkL":
                self.l, self.b, self.w, self.h = 50, 50*6, 50, 50
                self.frame_count, self.frame_begin = 18, 0
                self.clip_loop = True
            elif self.image_sprite == "runR":
                self.l, self.b, self.w, self.h = 50, 50*5, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.clip_loop = True
            elif self.image_sprite == "runL":
                self.l, self.b, self.w, self.h = 50, 50*4, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.clip_loop = True
            elif self.image_sprite == "swimR":
                self.l, self.b, self.w, self.h = 50, 50*3, 50, 50
                self.frame_count, self.frame_begin = 9, 0
                self.clip_loop = True
            elif self.image_sprite == "swimL":
                self.l, self.b, self.w, self.h = 50, 50*2, 50, 50
                self.frame_count, self.frame_begin = 9, 0
                self.clip_loop = True
            elif self.image_sprite == "hang":
                self.l, self.b, self.w, self.h = 50, 50*1, 50, 50
                self.frame_count, self.frame_begin = 6, 0
                self.clip_loop = True
            elif self.image_sprite == "climb":
                self.l, self.b, self.w, self.h = 50, 50*0, 50, 50
                self.frame_count, self.frame_begin = 14, 0
                self.clip_loop = True
            elif self.image_sprite == "jumpR_up":
                self.l, self.b, self.w, self.h = 50, 50*7, 50, 50
                self.frame_count, self.frame_begin = 1, 18
                self.clip_loop = False
            elif self.image_sprite == "jumpR_down":
                self.l, self.b, self.w, self.h = 50, 50*7, 50, 50
                self.frame_count, self.frame_begin = 1, 19
                self.clip_loop = False
            elif self.image_sprite == "jumpL_up":
                self.l, self.b, self.w, self.h = 50, 50*6, 50, 50
                self.frame_count, self.frame_begin = 1, 18
                self.clip_loop = False
            elif self.image_sprite == "jumpL_down":
                self.l, self.b, self.w, self.h = 50, 50*6, 50, 50
                self.frame_count, self.frame_begin = 1, 19
                self.clip_loop = False
            elif self.image_sprite == "die":
                self.l, self.b, self.w, self.h = 50, 50*0, 50, 50
                self.frame_count, self.frame_begin = 1, 14
                self.clip_loop = False

            else:
                self.l, self.b, self.w, self.h = 50, 50*0, 50, 50
                self.frame_count, self.frame_begin = 1, 26
                self.clip_loop = False

        elif self.image_id == PC_MARIO_SUPER:
            if self.image_sprite == "stayR":
                self.l, self.b, self.w, self.h = 50, 100 * 9, 50, 100
                self.frame_count, self.frame_begin = 27, 0
                self.clip_loop = True
            elif self.image_sprite == "stayL":
                self.l, self.b, self.w, self.h = 50, 100 * 8, 50, 100
                self.frame_count, self.frame_begin = 27, 0
                self.clip_loop = True
            elif self.image_sprite == "walkR":
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 18, 0
                self.clip_loop = True
            elif self.image_sprite == "walkL":
                self.l, self.b, self.w, self.h = 50, 100 * 6, 50, 100
                self.frame_count, self.frame_begin = 18, 0
                self.clip_loop = True
            elif self.image_sprite == "runR":
                self.l, self.b, self.w, self.h = 100, 100 * 5, 100, 100
                self.frame_count, self.frame_begin = 8, 0
                self.clip_loop = True
            elif self.image_sprite == "runL":
                self.l, self.b, self.w, self.h = 100, 100 * 4, 100, 100
                self.frame_count, self.frame_begin = 8, 0
                self.clip_loop = True
            elif self.image_sprite == "swimR":
                self.l, self.b, self.w, self.h = 100, 100 * 3, 100, 100
                self.frame_count, self.frame_begin = 9, 0
                self.clip_loop = True
            elif self.image_sprite == "swimL":
                self.l, self.b, self.w, self.h = 100, 100 * 2, 100, 100
                self.frame_count, self.frame_begin = 9, 0
                self.clip_loop = True
            elif self.image_sprite == "hang":
                self.l, self.b, self.w, self.h = 50, 100 * 1, 50, 100
                self.frame_count, self.frame_begin = 6, 0
                self.clip_loop = True
            elif self.image_sprite == "climb":
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 14, 0
                self.clip_loop = True
            elif self.image_sprite == "crawlR":
                self.l, self.b, self.w, self.h = 50, 100 * 9, 50, 100
                self.frame_count, self.frame_begin = 3, 27
                self.clip_loop = False
            elif self.image_sprite == "crawlL":
                self.l, self.b, self.w, self.h = 50, 100 * 8, 50, 100
                self.frame_count, self.frame_begin = 3, 27
                self.clip_loop = False
            elif self.image_sprite == "jumpR_up":
                self.l, self.b, self.w, self.h = 100, 100 * 7, 100, 100
                self.frame_count, self.frame_begin = 1, 18//2
                self.clip_loop = False
            elif self.image_sprite == "jumpR_down":
                self.l, self.b, self.w, self.h = 100, 100 * 7, 100, 100
                self.frame_count, self.frame_begin = 1, 20//2
                self.clip_loop = False
            elif self.image_sprite == "jumpL_up":
                self.l, self.b, self.w, self.h = 100, 100 * 6, 100, 100
                self.frame_count, self.frame_begin = 1, 18//2
                self.clip_loop = False
            elif self.image_sprite == "jumpL_down":
                self.l, self.b, self.w, self.h = 100, 100 * 6, 100, 100
                self.frame_count, self.frame_begin = 1, 20//2
                self.clip_loop = False
            else:
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 1, 29
                self.clip_loop = False

        elif self.image_id == PC_DRY_BONES:
            if self.image_sprite == "stayR":
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 1, 0
                self.clip_loop = False
            elif self.image_sprite == "stayL":
                self.l, self.b, self.w, self.h = 50, 100 * 6, 50, 100
                self.frame_count, self.frame_begin = 1, 0
                self.clip_loop = False
            elif self.image_sprite == "walkR":
                self.l, self.b, self.w, self.h = 50, 100 * 5, 50, 100
                self.frame_count, self.frame_begin = 16, 0
                self.clip_loop = True
            elif self.image_sprite == "walkL":
                self.l, self.b, self.w, self.h = 50, 100 * 4, 50, 100
                self.frame_count, self.frame_begin = 16, 0
                self.clip_loop = True
            elif self.image_sprite == "breakR":
                self.l, self.b, self.w, self.h = 50, 100 * 3, 50, 100
                self.frame_count, self.frame_begin = 12, 0
                self.clip_loop = False
            elif self.image_sprite == "breakL":
                self.l, self.b, self.w, self.h = 50, 100 * 2, 50, 100
                self.frame_count, self.frame_begin = 12, 0
                self.clip_loop = False
            elif self.image_sprite == "restoreR":
                self.l, self.b, self.w, self.h = 50, 100 * 1, 50, 100
                self.frame_count, self.frame_begin = 15, 0
                self.clip_loop = False
            elif self.image_sprite == "restoreL":
                self.l, self.b, self.w, self.h = 50, 100 * 0, 50, 100
                self.frame_count, self.frame_begin = 15, 0
                self.clip_loop = False
            else:
                self.l, self.b, self.w, self.h = 50, 100 * 7, 50, 100
                self.frame_count, self.frame_begin = 1, 15
                self.clip_loop = False

        elif self.image_id == PC_GOOMBA:
            if self.image_sprite == "stayR":
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.clip_loop = False
            elif self.image_sprite == "stayL":
                self.l, self.b, self.w, self.h = 50, 50 * 4, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.clip_loop = False
            elif self.image_sprite == "walkR":
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 16, 0
                self.clip_loop = True
            elif self.image_sprite == "walkL":
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 16, 0
                self.clip_loop = True
            elif self.image_sprite == "dieA":
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 3, 0
                self.clip_loop = False
            elif self.image_sprite == "dieB":
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.clip_loop = False
            else:
                self.l, self.b, self.w, self.h = 50, 50 * 5, 50, 50
                self.frame_count, self.frame_begin = 1, 15
                self.clip_loop = False

        elif self.image_id == PC_BOO:
            if self.image_sprite == "stayR":
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.clip_loop = False
            elif self.image_sprite == "stayL":
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 1, 0
                self.clip_loop = False
            elif self.image_sprite == "flyR":
                self.l, self.b, self.w, self.h = 50, 50 * 1, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.clip_loop = True
            elif self.image_sprite == "flyL":
                self.l, self.b, self.w, self.h = 50, 50 * 0, 50, 50
                self.frame_count, self.frame_begin = 8, 0
                self.clip_loop = True
            elif self.image_sprite == "dieR":
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 1
                self.clip_loop = False
            elif self.image_sprite == "dieL":
                self.l, self.b, self.w, self.h = 50, 50 * 2, 50, 50
                self.frame_count, self.frame_begin = 1, 1
                self.clip_loop = False
            else:
                self.l, self.b, self.w, self.h = 50, 50 * 3, 50, 50
                self.frame_count, self.frame_begin = 1, 7
                self.clip_loop = False

        elif self.image_id == PC_PIRANHA_PLANT:
            if self.image_sprite == "pop":
                self.frame_count, self.frame_begin = 78, 0
                self.l, self.b, self.w, self.h = 50, 100 * 4, 50, 50
                self.clip_loop = False


        self.frames = self.frame_begin
