from pico2d import *
from character_object import *


class enGoomba( Character_Object ):
    def __init__( self, x, y ):
        super(enGoomba, self).__init__()
        self.x, self.y = x, y
        # self.px, self.py = self.x, self.y
        self.image_id = CO_GOOMBA
        self.direction = D_RIGHT
        self.speed = 3
        self.set_clip("walk")

        self.is_walk = True

    def update_animation( self ):

        if self.is_walk:
            self.set_clip('walk')

    def update_move( self ):
        self.x += self.speed * self.direction
        if self.x < 0 or self.x > 799:  # fix point
            self.direction *= -1

        self.hit_box.set_pos(self.x, self.y)
        self.attack_box.set_pos(self.x, self.y)
        self.break_box.set_pos(self.x, self.y)

    def update( self ):
        self.update_move()
        self.update_animation()
