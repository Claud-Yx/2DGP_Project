from pico2d import *
from test_character import *

DISPLAY_W = 300
DISPLAY_H = 300

open_canvas(DISPLAY_W, DISPLAY_H)

bg = load_image('background\\castle1.png')
tester = Test()

Running = True

while Running:
    clear_canvas()
    bg.draw(DISPLAY_W // 2, DISPLAY_H // 2)
    tester.clip_draw( DISPLAY_W // 2, DISPLAY_H // 2 )
    tester.frame_update()
    update_canvas()
    Running = tester.handle_events()
    delay(0.05)

close_canvas()
