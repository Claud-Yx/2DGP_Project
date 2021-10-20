from player import *
from enemy_goomba import *
from enemy_drybones import *
from pico2d import *
import test_keyboard

open_canvas()

# Initialization:
player = Player(400, 100, PS_SUPER)
goomba = enGoomba(450, 300)
drybone = enDryBones(350, 325)

background = load_image('resource\\background\\castle1.png')
test_keyboard.keyboard_init()

Running = True

# Main Loop:
while Running:
    clear_canvas()

    background.draw(400, 300)

    player.update()
    player.clip_draw()
    player.frame_update()

    goomba.update()
    goomba.clip_draw()
    goomba.frame_update()

    drybone.update()
    drybone.clip_draw()
    drybone.frame_update()

    events = get_events()

    test_keyboard.update_test_keyboard()
    update_canvas()
    Running = player.handle_event(events)
    test_keyboard.keyboard_handle(events)

    delay(0.05)

close_canvas()