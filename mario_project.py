from player import *
from enemy_goomba import *
from enemy_drybones import *
from tileset_object import *
from pico2d import *
import test_keyboard

open_canvas()

# Initialization:
player = Player(250, 140, PS_SUPER)
goomba = enGoomba(450, 310)
drybone = enDryBones(350, 335)

# map tile set
box_100x100 = [TileSet(MT_BLOCK100X100) for i in range(16)]

for i in range(0, 8):
    box_100x100[i].set_pos(i * 100 + 50, 50)

for i in range(8, 16):
    box_100x100[i].set_pos((i-8) * 100 + 50, 250)

background = load_image('resource\\background\\castle1.png')
test_keyboard.keyboard_init()

Running = True

# Main Loop:
while Running:
    clear_canvas()

    background.draw(400, 300)

    for i in range( len( box_100x100 ) ):
        box_100x100[i].draw()

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