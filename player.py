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
        self.dir = D_RIGHT
        self.speed = 5
        self.state = s
        self.set_clip()

    def change_state( self ):
        if self.state == PS_SMALL:
            self.image_id = CO_MARIO_SMALL
        elif self.state == PS_SUPER:
            self.image_id = CO_MARIO_SUPER

    def update( self ):
        self.change_state()
        if self.action == "walk":
            if self.dir == D_RIGHT:
                self.x += self.speed
            elif self.dir == D_LEFT:
                self.x -= self.speed


    def handle_event( self ):

        events = get_events()

        for event in events:
            if event.type == SDL_QUIT:
                return False

            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    return False

                elif event.key == SDLK_RIGHT:
                    self.dir = D_RIGHT
                    self.action = "walk"
                    self.set_clip()
                elif event.key == SDLK_LEFT:
                    self.dir = D_LEFT
                    self.action = "walk"
                    self.set_clip()
                elif event.key == SDLK_UP:
                    pass
                elif event.key == SDLK_DOWN:
                    if self.state != PS_SMALL:
                        self.action = "crawl"
                        self.set_clip()

            elif event.type == SDL_KEYUP:

                if event.key == SDLK_RIGHT:
                    self.action = "stay"
                    self.set_clip()
                elif event.key == SDLK_LEFT:
                    self.action = "stay"
                    self.set_clip()
                elif event.key == SDLK_UP:
                    pass
                elif event.key == SDLK_DOWN:
                    if self.state != PS_SMALL:
                        self.action = "stay"
                        self.set_clip()

        return True
