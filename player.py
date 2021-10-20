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
        self.speed = 5
        self.state = s
        self.update_state()
        self.set_clip()

        self.is_crawl = False

    def update_state( self ):
        if self.state == PS_SMALL:
            self.image_id = CO_MARIO_SMALL
        elif self.state == PS_SUPER:
            self.image_id = CO_MARIO_SUPER

    def update_move( self ):
        if self.is_crawl:
            return
        if self.moving_dir == D_NONE:
            if self.action == "walk":
                self.set_clip("stay")
        else:
            if self.action == "stay":
                self.set_clip("walk")
            if self.direction != self.moving_dir:
                self.direction = self.moving_dir
                self.set_clip()
            self.x += self.speed * self.moving_dir

    def update( self ):
        self.update_state()
        self.update_move()


    def handle_event( self ):

        events = get_events()

        for event in events:
            if event.type == SDL_QUIT:
                return False

            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    return False

                elif event.key == SDLK_RIGHT:
                    self.direction = D_RIGHT
                    self.moving_dir += D_RIGHT
                    if not self.is_crawl:
                        self.set_clip("walk")
                elif event.key == SDLK_LEFT:
                    self.direction = D_LEFT
                    self.moving_dir += D_LEFT
                    if not self.is_crawl:
                        self.set_clip("walk")
                elif event.key == SDLK_UP:
                    pass
                elif event.key == SDLK_DOWN:
                    if self.state != PS_SMALL:
                        self.is_crawl = True
                        self.set_clip("crawl")

            elif event.type == SDL_KEYUP:

                if event.key == SDLK_RIGHT:
                    self.moving_dir += D_LEFT
                elif event.key == SDLK_LEFT:
                    self.moving_dir += D_RIGHT
                elif event.key == SDLK_UP:
                    pass
                elif event.key == SDLK_DOWN:
                    if self.state != PS_SMALL:
                        self.is_crawl = False
                        self.set_clip("stay")

        return True
