from ob_player import *
from ob_tileset import *
from ob_background import *
from ob_enemy import *

from pico2d import *
import test_keyboard

from collision import *
import gs_title

import gs_framework
import object_manager

name = "StageMainState"

player: Player = None
enemies: List[Enemy]
tiles = []

background: Background

show_bb = False


def enter():
    print("stage_main enter")
    # Initialization:
    global background
    background = Background()
    object_manager.add_object(background, object_manager.OL_BACKGROUND)

    global enemies
    enemies = []
    enemies.append(Goomba(950, 450))
    object_manager.add_objects(enemies, object_manager.OL_FOREGROUND)

    global player
    player = Player(TID.MARIO_SUPER, 200, 500)
    object_manager.add_object(player, object_manager.OL_FOREGROUND)

    global tilesxx
    tiles = []
    for x in range(50, gs_framework.canvas_width, 100):
        tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, x, 50))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 350, 150))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 350, 250))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 350, 350))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 250, 150))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 450, 150))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 450, 250))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 650, 350))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 750, 350))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 750, 450))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 850, 350))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 950, 350))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 1050, 350))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 1050, 450))
    object_manager.add_objects(tiles, object_manager.OL_TILESET)

    test_keyboard.keyboard_init()


def exit():
    global player, enemies, tiles
    global background

    del player
    del enemies
    del tiles
    del background


def handle_events():
    global show_bb

    for event in gs_framework.Events:
        if event.type == SDL_QUIT:
            gs_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            print(exit.__name__)
            gs_framework.change_state(gs_title)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F2):
            if not show_bb:
                show_bb = True
                for obj in object_manager.all_objects():
                    obj.show_bb = True
            else:
                show_bb = False
                for obj in object_manager.all_objects():
                    obj.show_bb = False
        else:
            player.handle_event(event)
            test_keyboard.keyboard_handle(gs_framework.Events)

def update():
    for obj in object_manager.all_objects():
        obj.update()

    # collision check
    collide_player_to_tiles(player, tiles)
    collide_enemies_to_tiles(enemies, tiles)


def draw():

    clear_canvas()

    # Draw
    for obj in object_manager.all_objects():
        try:
            obj.draw()
        except:
            print(obj.__name__)
            exit(-1)

    # Debug output
    # F2: Tile sets hit box
    keyboard_size = 0.75
    test_keyboard.update_test_keyboard(
        pico2d.get_canvas_width() - (64 * 4 + 50) * keyboard_size,
        pico2d.get_canvas_height() - 50 * keyboard_size,
        keyboard_size, keyboard_size
    )

    update_canvas()

def pause():
    pass

def resume():
    pass
