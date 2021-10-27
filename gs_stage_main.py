import gs_framework

from player import *
from enemy_goomba import *
from enemy_drybones import *
from tileset_object import *
from pico2d import *
import threading
import test_keyboard

import gs_title

name = "StageMainState"

player = None
enemies = []
tilesets = []

background = None

# Thread
running_thread = True
UpdateFrameThd = None

def enter():
    # Initialization:
    global player, enemies, tilesets
    global background
    global UpdateFrameThd, running_thread

    running_thread = True
    UpdateFrameThd = threading.Thread(target=UpdateFrame, name="FrameUpdater", daemon=True)

    player = Player(250, 340, PS_SUPER)
    enemies = []
    enemies.append(enGoomba(450, 310))
    enemies.append(enDryBones(350, 335))

    # Map tile set
    tilesets = [TileSet(MT_BLOCK100X100) for i in range(15)]

    for i in range(0, 8):
        tilesets[i].set_pos(i * 100 + 50, 50)

    tilesets[8].set_pos(250, 150)
    tilesets[9].set_pos(350, 150)
    tilesets[10].set_pos(450, 150)
    tilesets[11].set_pos(550, 150)
    tilesets[12].set_pos(450, 250)
    tilesets[13].set_pos(250, 350)
    tilesets[14].set_pos(450, 350)

    # Background
    background = load_image('resource\\background\\castle1.png')

    # Debugging virtual keyboard
    test_keyboard.keyboard_init()


def exit():
    global player, enemies, tilesets
    global background

    del player
    del enemies
    del tilesets
    del background


def handle_events():
    global running_thread

    if not player.handle_event(gs_framework.Events):
        running_thread = False
        gs_framework.change_state(gs_title)
    test_keyboard.keyboard_handle(gs_framework.Events)

def update():
    global player, enemies, tilesets
    global background

    # Update player
    player.update()

    # Update world
    update_world()
    player.update_hit_box()

    # Update enemies
    for enemy in enemies:
        enemy.update()

    # Debug output
    # F2: Tile sets hit box
    # F3: Character, item, interactive hit box
    test_keyboard.update_test_keyboard(
        pico2d.get_canvas_width() - (64 * 4 + 50) * 0.75,
        pico2d.get_canvas_height() - 50 * 0.75,
        0.75, 0.75
    )


def draw():
    global player, enemies, tilesets
    global background

    clear_canvas()

    # Draw background
    background.draw(gs_framework.canvas_width // 2, gs_framework.canvas_height // 2)

    # Draw tilesets
    for i in range(len(tilesets)):
        tilesets[i].draw()

    # Draw player
    player.clip_draw()

    # Draw enemies
    for enemy in enemies:
        enemy.clip_draw()

    # Draw debugging info
    show_hit_box()

    update_canvas()

    set_fps()

def pause():
    pass

def resume():
    pass


def update_world():
    for box in tilesets:
        player.hit_box.check_hit(box.hit_box)
        player.stand_box.check_hit(box.hit_box)


def show_hit_box():
    if player.is_show_hit_box:
        player.hit_box.show_hit_box()
        player.attack_box.show_hit_box()
        player.break_box.show_hit_box()

        for enemy in enemies:
            enemy.hit_box.show_hit_box()
            enemy.attack_box.show_hit_box()
            enemy.break_box.show_hit_box()

    if player.is_show_object_box:
        for box in tilesets:
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


def UpdateFrame():
    global player, enemies
    global background
    global running_thread

    while running_thread:
        player.update_frame()
        for enemy in enemies:
            enemy.update_frame()

        delay(1 / 20)