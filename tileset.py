from pico2d import *

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

        # Hit Box Size
        self.hit_x1, self.hit_x2 = 25, 25
        self.hit_y1, self.hit_y2 = 25, 25

        # Image Sprite
        self.image = load_image('resource\\no_image.png')
        self.image_id = id

        if self.image_id != MT_NONE:
            self.set_tile(self.image_id)

    def set_hit_box( self, x1, x2, y1, y2 ):
        self.hit_x1 = x1
        self.hit_x2 = x2
        self.hit_y1 = y1
        self.hit_y2 = y2

    def set_pos( self, x, y ):
        self.x = x
        self.y = y

    def set_tile( self, id ):
        if id == MT_BLOCK50X50:
            self.image = load_image('resource\\maptile\\block50x50.png')
            self.set_hit_box(25, 25, 25, 25)
        elif id == MT_BLOCK50X100:
            self.image = load_image('resource\\maptile\\block50x100.png')
            self.set_hit_box(25, 25, 50, 50)
        elif id == MT_BLOCK100X50:
            self.image = load_image('resource\\maptile\\block100x50.png')
            self.set_hit_box(50, 50, 25, 25)
        elif id == MT_BLOCK100X100:
            self.image = load_image('resource\\maptile\\block100x100.png')
            self.set_hit_box(50, 50, 50, 50)

    def get_hit_box( self ):
        return [self.x - self.hit_x1, self.x + self.hit_x2,
                self.y - self.hit_y1, self.y + self.hit_y2]

    def draw( self ):
        self.image.draw(self.x, self.y)