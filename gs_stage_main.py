import server

import ob_foreground
import object_manager
from pico2d import *

import stage_manager as sm
import test_keyboard

from collision import *
import gs_title
import ob_map

import gs_framework

import map_edit

name = "StageMainState"

show_bb = False


def enter():
    import ob_background
    # Initialization:
    # server.init()

    map_edit.create_map()

    # server.stage = sm.stage[sm.Stage.stage_num, sm.Stage.map_num].map
    # object_manager.objects = sm.stage[sm.Stage.stage_num, sm.Stage.map_num].objects
    #
    # for o in object_manager.all_objects():
    #     if isinstance(o, ob_background.Background):
    #         server.background = o
    #     elif isinstance(o, ob_player.Player):
    #         server.player = o
    #     elif isinstance(o, ob_enemy.Enemy):
    #         server.enemies.append(o)
    #     elif isinstance(o, ob_tileset.TileSet):
    #         server.tiles.append(o)
    #     elif isinstance(o, ob_item.Item):
    #         server.items.append(o)
    #     elif isinstance(o, ob_interactive.WireMesh):
    #         server.interactives.append(o)
    #     elif isinstance(o, ob_foreground.Foreground):
    #         server.foreground.append(o)

    game_object.init()

    test_keyboard.keyboard_init()

    server.start_time = gs_framework.frame_time


def exit():
    object_manager.destroy()
    server.destroy()


def handle_events():

    for event in gs_framework.Events:
        if event.type == SDL_QUIT:
            gs_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            gs_framework.change_state(gs_title)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F2):
            if not server.show_bb:
                server.show_bb = True
                for obj in object_manager.all_objects():
                    obj.show_bb = True
            else:
                server.show_bb = False
                for obj in object_manager.all_objects():
                    obj.show_bb = False
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F3):
            server.stage.print_index()

        else:
            server.player.handle_event(event)
            test_keyboard.keyboard_handle(gs_framework.Events)


def update():
    # s_time = get_time()
    server.current_time = get_time() - server.start_time

    # if server.show_bb:
    #     for obj in object_manager.all_objects():
    #         obj.show_bb = True
    # else:
    #     for obj in object_manager.all_objects():
    #         obj.show_bb = False

    if server.time_stop:
        for obj in object_manager.all_objects():
            obj.is_time_stop = True
    else:
        for obj in object_manager.all_objects():
            obj.is_time_stop = False

    for obj in object_manager.all_objects():
        if obj.update() == -1:
            return

    # indexing
    server.stage.update()

    # if stage_prev_x != server.stage.x:
    #     print("map pos: (%.2f, %.2f)" % (server.stage.x, server.stage.y))

    # collision check
    # player collision indexing
    server.player.nearby_tiles.clear()
    server.player.nearby_enemies.clear()
    server.player.nearby_items.clear()
    server.player.nearby_interactives.clear()

    player_index_x = int(server.player.ax // ob_map.TILE_WIDTH)
    player_index_y = int(server.player.ay // ob_map.TILE_HEIGHT)
    for x in range(player_index_x - 2, player_index_x + 2):
        if x < 0 or len(server.stage.object_index) <= x:
            continue

        for y in range(player_index_y - 2, player_index_y + 2):
            if y < 0 or len(server.stage.object_index[x]) <= y:
                continue

            nearby_list = server.stage.object_index[x][y]
            for obj in nearby_list:
                obj: game_object.GameObject
                if obj.type_name == TN.TILESETS:
                    server.player.nearby_tiles.add(obj)
                elif obj.type_name == TN.ENEMIES:
                    server.player.nearby_enemies.add(obj)
                elif obj.type_name == TN.ITEMS:
                    server.player.nearby_items.add(obj)
                elif obj.type_name == TN.INTERACTIVES:
                    server.player.nearby_interactives.add(obj)

    # player collision check
    # player to tile sets
    for floor in server.player.nearby_tiles:
        if collide_player_to_floor(server.player, floor):
            break
    for ceiling in server.player.nearby_tiles:
        if server.player.is_jump or server.player.cur_state == ob_player.ClimbState:
            if collide_player_to_ceiling(server.player, ceiling):
                break
    for tile in server.player.nearby_tiles:
        if collide_player_to_right_wall(server.player, tile):
            break
    for tile in server.player.nearby_tiles:
        if collide_player_to_left_wall(server.player, tile):
            break

    # player to enemy
    for enemy in server.player.nearby_enemies:
        enemy: ob_enemy.Enemy
        if stomp_player_to_enemy(server.player, enemy):
            break

    for enemy in server.player.nearby_enemies:
        enemy: ob_enemy.Enemy
        if hit_enemy_to_player(server.player, enemy):
            break

    # player to item
    for item in server.player.nearby_items:
        item: ob_item.Item
        if collide_item_to_player(server.player, item):
            break

    # player to interactive
    for itr in server.player.nearby_interactives:
        if collide_player_to_interactive(server.player, itr):
            break

    # if len(server.player.nearby_tiles) != 0:
    #     print(server.player.nearby_tiles)

    # enemy collision checking and indexing
    for enemy in server.enemies:
        if isinstance(enemy, ob_enemy.Boo):
            continue

        enemy.nearby_tiles.clear()

        enemy_index_x = int(enemy.ax // ob_map.TILE_WIDTH)
        enemy_index_y = int(enemy.ay // ob_map.TILE_HEIGHT)

        for x in range(enemy_index_x - 2, enemy_index_x + 2):
            if x < 0 or len(server.stage.object_index) <= x:
                continue

            for y in range(enemy_index_y - 2, enemy_index_y + 2):
                if y < 0 or len(server.stage.object_index[x]) <= y:
                    continue

                nearby_list = server.stage.object_index[x][y]
                for obj in nearby_list:
                    obj: game_object.GameObject
                    if obj.type_name == TN.TILESETS:
                        enemy.nearby_tiles.add(obj)

        # enemy to floor tile
        for floor in enemy.nearby_tiles:
            if collide_enemy_to_floor(enemy, floor):
                break

        # enemy to wall tile
        for tile in enemy.nearby_tiles:
            if collide_enemy_to_wall(enemy, tile):
                break

        if isinstance(enemy, ob_enemy.DryBones) and enemy.dead_type is None:
            is_cliff = None
            for tile in enemy.nearby_tiles:
                is_cliff = check_enemy_to_cliff(enemy, tile)
                if not is_cliff:
                    break
            if is_cliff:
                enemy.x_direction *= -1
                enemy.facing = enemy.x_direction
                enemy.set_info()

    # item collision checking and indexing
    for item in server.items:
        if item.type_id == TID.COIN:
            continue

        item.nearby_tiles.clear()

        item_index_x = int(item.ax // ob_map.TILE_WIDTH)
        item_index_y = int(item.ay // ob_map.TILE_HEIGHT)

        for x in range(item_index_x - 2, item_index_x + 2):
            if x < 0 or len(server.stage.object_index) <= x:
                continue

            for y in range(item_index_y - 2, item_index_y + 2):
                if y < 0 or len(server.stage.object_index[x]) <= y:
                    continue

                nearby_list = server.stage.object_index[x][y]
                for obj in nearby_list:
                    obj: game_object.GameObject
                    if obj.type_name == TN.TILESETS:
                        item.nearby_tiles.add(obj)

        # item to floor tile
        for floor in item.nearby_tiles:
            if collide_item_to_floor(item, floor):
                break

        # item to ceiling tile
        for ceiling in item.nearby_tiles:
            if collide_item_to_ceiling(item, ceiling):
                break

        # item to wall tile
        for wall in item.nearby_tiles:
            if collide_item_to_wall(item, wall):
                break

    # e_time = get_time() - s_time
    # print(e_time)


def draw():
    clear_canvas()

    # Draw
    for obj in object_manager.all_objects():
        # try:
        obj.draw()
        # except:
        #     print(obj.__class__.__name__)
        #     exit()

    debug_print_2 = load_font('resource\\font\\new_super_mario_font.ttf', 26)
    debug_print_2.draw(6, gs_framework.canvas_height - 16,
                       "LIFE: %3d           COIN: %3d           SCORE: %.7d                                                                                                           TIME: %3d" %
                       (server.player.life, server.player.coin, server.player.score,
                        int(server.stage.timer_stage)),
                       (255, 255, 255))

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
