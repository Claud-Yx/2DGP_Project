from player import *
from enemy_goomba import *
from enemy_drybones import *
from tileset_object import *
from pico2d import *
import threading
import test_keyboard


def show_hit_box():
    if player.is_show_hit_box:
        player.hit_box.show_hit_box()
        player.attack_box.show_hit_box()
        player.break_box.show_hit_box()

        goomba.hit_box.show_hit_box()
        goomba.attack_box.show_hit_box()
        goomba.break_box.show_hit_box()

        drybone.hit_box.show_hit_box()
        drybone.attack_box.show_hit_box()
        drybone.break_box.show_hit_box()

    if player.is_show_object_box:
        for box in box_100x100:
            box.hit_box.show_hit_box()


def set_fps(fps=60):
    pass


open_canvas()

# Initialization:
player = Player(250, 140, PS_SUPER)
goomba = enGoomba(450, 310)
drybone = enDryBones(350, 335)

# Map tile set
box_100x100 = [TileSet(MT_BLOCK100X100) for i in range(16)]

for i in range(0, 8):
    box_100x100[i].set_pos(i * 100 + 50, 50)

for i in range(8, 16):
    box_100x100[i].set_pos((i-8) * 100 + 50, 250)

# Background
background = load_image('resource\\background\\castle1.png')

# Debugging virtual keyboard
test_keyboard.keyboard_init()

Running = True

events = None

def Rendering():
    global player, goomba, drybone
    global background
    global box_100x100
    global Running

    while Running:
        print_fps()

        clear_canvas()

        background.draw( 400, 300 )

        for i in range( len( box_100x100 ) ):
            box_100x100[ i ].draw()

        player.clip_draw()
        goomba.clip_draw()
        drybone.clip_draw()

        test_keyboard.update_test_keyboard()

        show_hit_box()

        debug_print(str(get_time()))

        update_canvas()


RenderingTrd = threading.Thread( target = Rendering, name = "Update", daemon = True )
RenderingTrd.start()

# Main Loop:
while Running:

    # clear_canvas()

    # background.draw(400, 300)
    #
    # for i in range( len( box_100x100 ) ):
    #     box_100x100[i].draw()

    player.update()
    # player.clip_draw()
    player.update_frame()

    goomba.update()
    # goomba.clip_draw()
    goomba.update_frame()

    drybone.update()
    # drybone.clip_draw()
    drybone.update_frame()
    #
    # test_keyboard.update_test_keyboard()
    #
    # show_hit_box()

    # update_canvas()

    events = get_events()
    Running = player.handle_event(events)
    test_keyboard.keyboard_handle(events)

    # set_fps
    delay(1 / 40)

close_canvas()