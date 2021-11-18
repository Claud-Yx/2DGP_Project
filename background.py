from value import *
from pico2d import *

import gs_framework

class Background:
    image = None

    def __init__(self):
        if Background.image is None:
            Background.image = load_image('resource\\background\\castle1.png')
    
    def update(self):
        pass

    def draw(self):
        Background.image.draw(gs_framework.canvas_width // 2, gs_framework.canvas_height // 2)

    def handle_event(self):
        pass