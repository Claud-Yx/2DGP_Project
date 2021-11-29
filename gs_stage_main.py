import game_object
import ob_enemy
import server

from pico2d import *
import test_keyboard

from collision import *
import gs_title
import ob_map

import gs_framework
import object_manager

name = "StageMainState"

show_bb = False


def enter():
    # print("stage_main enter")
    # Initialization:
    server.init()
    object_manager.objects = [[], [], [], [], []]

    server.stage = ob_map.Map(0, 0)
    server.stage.set_size(gs_framework.canvas_width * 2,
                         222xzx gs_framework.canvas_height * 2)
    server.background = ob_background.Background()
    object_manager.add_object(server.background, object_manager.OL_BACKGROUND)

    # server.enemies.append(ob_enemy.Goomba(930, 460))
    # server.enemies.append(ob_enemy.Goomba(930, 460, DIR.LEFT))
    # server.enemies.append(ob_enemy.Goomba(970, 500, DIR.LEFT))
    server.enemies.append(ob_enemy.Goomba(900, 480))
    object_manager.add_objects(server.enemies, object_manager.OL_CHARACTER)

    server.player = ob_player.Player(TID.MARIO_SUPER, 200, 500)
    object_manager.add_object(server.player, object_manager.OL_CHARACTER)

    for x in range(150, gs_framework.canvas_width * 2, 100):
        server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, x, 50))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 350, 150))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 350, 250))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 350, 350))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 250, 150))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 450, 150))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 450, 250))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 650, 350))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 750, 350))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 750, 450))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 850, 350))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 950, 350))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 1050, 350))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 1050, 450))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 450, 325))
    object_manager.add_objects(server.tiles, object_manager.OL_TILESET)

    test_keyboard.keyboard_init()

    server.start_time = gs_framework.frame_time


def exit():
    object_manager.destroy()
    server.destroy()


def handle_events():
    global show_bb

    for event in gs_framework.Events:
        if event.type == SDL_QUIT:
            gs_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
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
            server.player.handle_event(event)
            test_keyboard.keyboard_handle(gs_framework.Events)


def update():
    # s_time = get_time()
    server.current_time = get_time() - server.start_time

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
    stage_prev_x = server.stage.x
    server.stage.update()

    # if stage_prev_x != server.stage.x:
    #     print("map pos: (%.2f, %.2f)" % (server.stage.x, server.stage.y))

    # collision check
    # player collision indexing
    server.player.nearby_tiles.clear()
    server.player.nearby_enemies.clear()

    player_index_x = int((server.player.x - server.stage.x) // ob_map.TILE_WIDTH)
    player_index_y = int(server.player.y // ob_map.TILE_HEIGHT)
    for x in range(player_index_x - 2, player_index_x + 2):
        if x < 0 or len(server.stage.object_index) <= x:
            continue

        for y in range(player_index_y - 2, player_index_y + 2):
            if y < 0 or len(server.stage.object_index[x]) <= y:
                continue

            nearby_list = server.stage.object_index[x][y]
            for obj in nearby_list:
                obj: game_object.Object
                if obj.type_name == TN.TILESETS:
                    server.player.nearby_tiles.add(obj)
                elif obj.type_name == TN.ENEMIES:
                    server.player.nearby_enemies.add(obj)

    # player collision check
    # player to tile sets
    for floor in server.player.nearby_tiles:
        if collide_player_to_floor(server.player, floor):
            break
    for ceiling in server.player.nearby_tiles:
        if server.player.is_jump:
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

    # if len(server.player.nearby_tiles) != 0:
    #     print(server.player.nearby_tiles)

    # enemy collision indexing
    for enemy in server.enemies:
        enemy.nearby_tiles.clear()

        enemy_index_x = int((enemy.x - server.stage.x) // ob_map.TILE_WIDTH)
        enemy_index_y = int(enemy.y // ob_map.TILE_HEIGHT)

        for x in range(enemy_index_x - 2, enemy_index_x + 2):
            if x < 0 or len(server.stage.object_index) <= x:
                continue

            for y in range(enemy_index_y - 2, enemy_index_y + 2):
                if y < 0 or len(server.stage.object_index[x]) <= y:
                    continue

                nearby_list = server.stage.object_index[x][y]
                for obj in nearby_list:
                    obj: game_object.Object
                    if obj.type_name == TN.TILESETS:
                        enemy.nearby_tiles.add(obj)

        for floor in enemy.nearby_tiles:
            if collide_enemy_to_floor(enemy, floor):
                break
        for tile in enemy.nearby_tiles:
            if collide_enemy_to_wall(enemy, tile):
                break

    # e_time = get_time() - s_time
    # print(e_time)


def draw():
    clear_canvas()

    # Draw
    for obj in object_manager.all_objects():
        try:
            obj.draw()
        except:
            print(obj.__name__)
            exit()

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
