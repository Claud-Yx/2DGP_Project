from pico2d import *
from character_object import *


class enDryBones( Character_Object ):
    def __init__( self, x, y ):
        super(enDryBones, self).__init__()
        self.x, self.y = x, y
        # self.px, self.py = self.x, self.y
        self.image_id = CO_DRY_BONES
        self.direction = D_LEFT
        self.speed = 2
        self.set_clip("walk")

        self.is_walk = True

    def update_animation( self ):

        if self.is_walk:
            self.set_clip('walk')

    def update_move( self ):
        self.x += self.speed * self.direction
        if self.x < 0 or self.x > 799:  # fix point
            self.direction *= -1

    def update( self ):
        self.update_move()
        self.update_animation()
