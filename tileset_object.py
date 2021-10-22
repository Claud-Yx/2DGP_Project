from pico2d import *
from hit_box import *

MT_NONE = 0
MT_BLOCK50X50 = 1
MT_BLOCK50X100 = 2
MT_BLOCK100X50 = 3
MT_BLOCK100X100 = 4
MT_PIPE = 5
MT_PIPE_END = 6

class TileSet:
    def __init__(self, id = MT_NONE, x = 0, y = 0):
        # Tile position
        self.x, self.y = x, y

        # Image Sprite
        self.image = load_image('resource\\no_image.png')
        self.image_id = id

        # Hit box
        self.hit_box = HitBox(self.x, self.y)

        if self.image_id != MT_NONE:
            self.set_tile(self.image_id)

    def set_pos( self, x, y ):
        self.x = x
        self.y = y
        self.hit_box.set_pos(self.x, self.y)

    def set_tile( self, id ):
        if id == MT_BLOCK50X50:
            self.image = load_image('resource\\tileset\\block50x50.png')
            self.hit_box.set_range(25, 25, 25, 25)
        elif id == MT_BLOCK50X100:
            self.image = load_image('resource\\tileset\\block50x100.png')
            self.hit_box.set_range(50, 50, 25, 25)
        elif id == MT_BLOCK100X50:
            self.image = load_image('resource\\tileset\\block100x50.png')
            self.hit_box.set_range(25, 25, 50, 50)
        elif id == MT_BLOCK100X100:
            self.image = load_image('resource\\tileset\\block100x100.png')
            self.hit_box.set_range(50, 50, 50, 50)

    def draw( self ):
        self.image.draw(self.x, self.y)