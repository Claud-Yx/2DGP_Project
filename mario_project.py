from player import *
from enemy_goomba import *
from enemy_drybones import *
from tileset import *
from pico2d import *
import test_keyboard

hxL = 0
hxR = 1
hyD = 2
hyU = 3

open_canvas()

def update_engine():
    global player, goomba, drybone
    global box_100x100

    for box in box_100x100:
        p_hb = player.get_hit_box()
        b_hb = box.get_hit_box()

        if b_hb[hxL] < p_hb[hxL]  < b_hb[hxR] or b_hb[hxL] < p_hb[hxR] < b_hb[hxR]:
            if b_hb[hyU] + 1 >= p_hb[hyD] > b_hb[hyD]:
                player.switch_fall(False)
                player.y = b_hb[hyU] + player.hit_y1 + 0.1
            elif p_hb[hyD] < b_hb[hyU]:
                continue
            else:
                player.switch_fall()

        elif b_hb[hyD] < p_hb[hyD] < b_hb[hyU] or b_hb[hyD] < p_hb[hyU] < b_hb[hyU]:
            if b_hb[hxR] + 1 >= p_hb[hxL] > b_hb[hxL]:
                player.x = b_hb[hxR ] + player.hit_x1 + 0.1
            elif b_hb[hxL ] - 1 <= p_hb[hxR ] >= b_hb[hxR ]:
                player.x = b_hb[hxL ] + player.hit_x2 + 0.1


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

    # update_engine()

    events = get_events()

    test_keyboard.update_test_keyboard()
    update_canvas()
    Running = player.handle_event(events)
    test_keyboard.keyboard_handle(events)

    delay(0.05)

close_canvas()