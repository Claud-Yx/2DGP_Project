from pico2d import *
from bounding_box import *
from value import *


class TileSet:
    image = None

    def __init__(self, id = TID.NONE, x = 0, y = 0):
        # Tile position
        self.x, self.y = x, y
        self.wx, self.wy = x, y

        # Image Sprite
        self.image_id = id

        # Hit box
        self.hit_box = HitBox(self.x, self.y, type=TYPE.PLATFORM_NT)

        if self.image_id != TID.NONE:
            self.set_tile()

        if TileSet.image == None:
            TileSet.image = [
                load_image('resource\\tileset\\block50x50.png'),
                load_image('resource\\tileset\\block50x100.png'),
                load_image('resource\\tileset\\block100x50.png'),
                load_image('resource\\tileset\\block100x100.png')
                ]

    def init_decode(self, mx, my):
        self.wx = mx
        self.wy = my

    def set_pos( self, x, y ):
        self.x = x
        self.y = y
        self.hit_box.set_pos(self.x, self.y)

    def set_tile( self ):
        if self.image_id == TID.CASTLE_BLOCK_50X50:
            self.hit_box.set_range(25, 25, 25, 25)
            self.hit_box.type_name = NAME.TILESET
        elif self.image_id == TID.CASTLE_BLOCK_50X100:
            self.hit_box.set_range(50, 50, 25, 25)
        elif self.image_id == TID.CASTLE_BLOCK_100X50:
            self.hit_box.set_range(25, 25, 50, 50)
        elif self.image_id == TID.CASTLE_BLOCK_100X100:
            self.hit_box.set_range(50, 50, 50, 50)

    def draw( self ):
        TileSet.image[self.image_id].draw(self.x, self.y)