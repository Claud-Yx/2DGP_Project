from pico2d import *

class Character:

    def __init__(self):
        self.x, self.y = 0, 0
        self.l, self.b, self.w, self.h = 0, 0, 0, 0
        self.image = load_image("resource\\No_Image.png")
        self.frames = 0
        self.frame_begin = 0
        self.frame_count = 0
        self.loop_animation = False
