from player import *
from enemy_goomba import *
from enemy_drybones import *
from tileset_object import *
from pico2d import *
import threading
import test_keyboard


# def enter():
#     pass
#
# def exit():
#     pass
#
#
# def handle_events():
#     pass
#
# def update():
#     pass
#
#
# def draw():
#     pass
#
# def pause():
#     pass
#
# def resume():
#     pass


def update_world():
    for box in box_100x100:
        player.hit_box.check_hit(box.hit_box)
        player.stand_box.check_hit(box.hit_box)


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


ct = 0.0
real_fps = 30
is_fps_changed = False


def set_fps(fps=30):
    global ct
    global real_fps
    global is_fps_changed

    if real_fps != fps and not is_fps_changed:
        real_fps = fps
        is_fps_changed = True

    delay(1 / real_fps)

    dt = get_time() - ct
    ct += dt
    dt = max(dt, 0.0001)
    cur_fps = 1.0 / dt

    if fps + 250 < cur_fps:
        real_fps -= 250
    elif fps + 50 < cur_fps:
        real_fps -= 50
    elif fps + 10 < cur_fps:
        real_fps -= 10
    elif fps + 5 < cur_fps:
        real_fps -= 5
    elif fps + 2 < cur_fps:
        real_fps -= 2
    elif fps + 0.4 < cur_fps:
        real_fps -= 0.4

    if fps - 250 > cur_fps:
        real_fps += 250
    elif fps - 50 > cur_fps:
        real_fps += 50
    elif fps - 10 > cur_fps:
        real_fps += 10
    elif fps - 5 < cur_fps:
        real_fps += 5
    elif fps - 2 > cur_fps:
        real_fps += 2
    elif fps - 0.4 > cur_fps:
        real_fps += 0.4


open_canvas(full=True)

# Initialization:
player = Player(250, 340, PS_SUPER)
goomba = enGoomba(450, 310)
drybone = enDryBones(350, 335)

# Map tile set
box_100x100 = [TileSet(MT_BLOCK100X100) for i in range(15)]

for i in range(0, 8):
    box_100x100[i].set_pos(i * 100 + 50, 50)

box_100x100[8].set_pos(250, 150)
box_100x100[9].set_pos(350, 150)
box_100x100[10].set_pos(450, 150)
box_100x100[11].set_pos(550, 150)
box_100x100[12].set_pos(450, 250)
box_100x100[13].set_pos(250, 350)
box_100x100[14].set_pos(450, 350)

# Background
background = load_image('resource\\background\\castle1.png')

# Debugging virtual keyboard
test_keyboard.keyboard_init()

Running = True


def RenderFrame():
    global player, goomba, drybone
    global background
    global box_100x100
    global Running

    while Running:
        player.update_frame()
        goomba.update_frame()
        drybone.update_frame()

        delay(1 / 20)


RenderFrameTrd = threading.Thread(target=RenderFrame, name="FrameRenderer", daemon=True)
RenderFrameTrd.start()

# Main Loop:
while Running:

    clear_canvas()

    background.draw(400, 300)

    for i in range(len(box_100x100)):
        box_100x100[i].draw()

    player.update()

    update_world()
    player.update_hit_box()
    player.clip_draw()

    # goomba.update()
    # goomba.clip_draw()
    #
    # drybone.update()
    # drybone.clip_draw()

    # Debug output
    # F2: Tile sets hit box
    # F3: Character, item, interactive hit box
    show_hit_box()
    test_keyboard.update_test_keyboard(
        pico2d.get_canvas_width() - (64 * 4 + 50) * 0.75,
        pico2d.get_canvas_height() - 50 * 0.75,
        0.75, 0.75
    )

    events = get_events()
    Running = player.handle_event(events)
    test_keyboard.keyboard_handle(events)

    update_canvas()

    set_fps()

close_canvas()
