from pico2d import *
from character_object import *

PS_SMALL = 0
PS_SUPER = 1

class Player( Character_Object ):
    def __init__(self, x, y, s = PS_SMALL):
        super(Player, self).__init__()
        self.x, self.y = x, y
        # self.px, self.py = self.x, self.y
        self.action = "stay"
        self.direction = D_RIGHT
        self.moving_dir = 0
        self.speed = 6
        self.acceleration = 3
        self.state = s
        self.update_state()
        self.set_clip()

        self.is_stay = True
        self.is_walk = False
        self.is_run = False
        self.is_crawl = False

    def switch_stay( self, bl = True ):
        self.is_stay = bl
        if self.is_stay:
            self.is_walk = False
        else:
            pass

    def switch_walk( self, bl = True ):
        self.is_walk = bl
        if self.is_walk:
            self.is_stay = False
        else:
            pass

    def switch_run( self, bl = True ):
        self.is_run = bl

    def switch_crawl( self, bl = True ):
        self.is_crawl = bl

    def update_state( self ):
        if self.state == PS_SMALL:
            self.image_id = CO_MARIO_SMALL
        elif self.state == PS_SUPER:
            self.image_id = CO_MARIO_SUPER

    def update_animation( self ):

        if self.is_walk:
            if self.is_run:
                self.set_clip('run')
            else:
                self.set_clip('walk')
        elif self.is_crawl:
            self.set_clip('crawl')
        elif self.is_stay:
            self.set_clip('stay')

    def update_move( self ):
        if self.moving_dir == D_NONE:
            if not self.is_stay:
                self.switch_stay()
        else:
            if self.is_stay:
                self.switch_walk(True)
            if self.direction != self.moving_dir:
                self.direction = self.moving_dir
                self.set_clip()

            if self.is_walk:
                if self.is_run:
                    self.x += (self.speed + self.acceleration) * self.moving_dir
                else:
                    self.x += self.speed * self.moving_dir

        # print("update move: ", self.direction, self.moving_dir, self.action)

    def update( self ):
        self.update_state()
        self.update_move()
        self.update_animation()

    def handle_event( self, events ):
        # events = get_events()

        for event in events:
            if event.type == SDL_QUIT:
                return False

            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    return False

                elif event.key == SDLK_RIGHT:
                    self.direction = D_RIGHT
                    self.moving_dir += D_RIGHT
                    self.switch_walk()
                elif event.key == SDLK_LEFT:
                    self.direction = D_LEFT
                    self.moving_dir += D_LEFT
                    self.switch_walk()
                elif event.key == SDLK_UP:
                    pass
                elif event.key == SDLK_DOWN:
                    if self.state != PS_SMALL:
                        self.switch_crawl()

                elif event.key == SDLK_z:
                    self.switch_run()

            elif event.type == SDL_KEYUP:

                if event.key == SDLK_RIGHT:
                    self.moving_dir += D_LEFT
                elif event.key == SDLK_LEFT:
                    self.moving_dir += D_RIGHT
                elif event.key == SDLK_UP:
                    pass
                elif event.key == SDLK_DOWN:
                    if self.state != PS_SMALL:
                        self.switch_crawl(False)

                elif event.key == SDLK_z:
                    self.switch_run(False)

        return True
