from player import *
from pico2d import *

open_canvas()

# Initialization:
player = Player(400, 100)
background = load_image('resource\\background\\castle1.png')

Running = True

# Main Loop:
while Running:
    clear_canvas()

    background.draw(400, 300)

    player.update()
    player.clip_draw()
    player.frame_update()

    update_canvas()
    Running = player.handle_event()
    delay(0.05)

close_canvas()