import object_manager

import ob_background
import server

from pico2d import *
import test_keyboard

from collision import *
import gs_title
import ob_map

import gs_framework

name = "StageMainState"

show_bb = False


def enter():
    # print("stage_main enter")
    # Initialization:
    server.init()
    object_manager.objects = [[], [], [], [], []]

    # stage map
    server.stage = ob_map.Map(0, 0)
    server.stage.set_size(gs_framework.canvas_width * 2,
                          gs_framework.canvas_height * 2)

    # background
    server.background = ob_background.Background()
    object_manager.add_object(server.background, L.BACKGROUND)

    # item
    server.items.append(ob_item.Coin(525, 125))
    server.items.append(ob_item.Coin(525, 175))
    server.items.append(ob_item.Coin(575, 125))
    server.items.append(ob_item.Coin(575, 175))
    # server.items.append(ob_item.SuperMushroom(800, 480))
    object_manager.add_objects(server.items, L.ITEMS)

    # enemy
    server.enemies.append(ob_enemy.DryBones(930, 660))
    server.enemies.append(ob_enemy.DryBones(430, 660))
    # server.enemies.append(ob_enemy.Goomba(930, 660, DIR.LEFT))
    server.enemies.append(ob_enemy.Goomba(970, 200, DIR.LEFT))
    server.enemies.append(ob_enemy.Goomba(900, 280))
    object_manager.add_objects(server.enemies, L.ENEMIES)

    # player
    server.player = ob_player.Player(TID.MARIO_SUPER, 100, 700)
    object_manager.add_object(server.player, object_manager.OL_CHARACTER)

    for x in range(150, gs_framework.canvas_width * 2, 100):
        server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, x, 50))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 350, 150))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 350, 250))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 350, 350))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 250, 150))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 450, 150))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 450, 250))
    # server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 650, 550))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 750, 550))
    # server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 750, 650))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 850, 550))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 950, 550))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 1050, 550))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 1150, 550))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 1250, 550))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 1250, 650))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 450, 325))

    server.tiles.append(ob_tileset.RandomBox(125, 375))
    server.tiles.append(ob_tileset.RandomBox(175, 375, item=TID.SUPER_MUSHROOM))
    server.tiles.append(ob_tileset.RandomBox(225, 375, state=ob_tileset.RS.INVISIBLE))
    # server.tiles.append(ob_tileset.RandomBox(475, 125, state=ob_tileset.RS.POLYMORPH))
    server.tiles.append(ob_tileset.RandomBox(1325, 325, state=ob_tileset.RS.INVISIBLE))
    server.tiles.append(ob_tileset.RandomBox(1375, 325, state=ob_tileset.RS.INVISIBLE))
    server.tiles.append(ob_tileset.RandomBox(1425, 325, state=ob_tileset.RS.INVISIBLE))
    server.tiles.append(ob_tileset.RandomBox(1475, 325, state=ob_tileset.RS.INVISIBLE))
    server.tiles.append(ob_tileset.RandomBox(1525, 275))
    server.tiles.append(ob_tileset.RandomBox(1575, 275, state=ob_tileset.RS.INVISIBLE))

    server.tiles.append(ob_tileset.Brick(125, 575))
    server.tiles.append(ob_tileset.Brick(175, 575))
    server.tiles.append(ob_tileset.Brick(225, 575))
    server.tiles.append(ob_tileset.RandomBox(275, 575, item=TID.SUPER_STAR, state=ob_tileset.RS.POLYMORPH))
    server.tiles.append(ob_tileset.Brick(325, 575))
    server.tiles.append(ob_tileset.Brick(375, 575))
    server.tiles.append(ob_tileset.Brick(425, 575))
    server.tiles.append(ob_tileset.Brick(475, 575))
    server.tiles.append(ob_tileset.Brick(525, 575))
    server.tiles.append(ob_tileset.Brick(575, 575))

    server.tiles.append(ob_tileset.Spike(625, 125))
    server.tiles.append(ob_tileset.Spike(675, 125))
    server.tiles.append(ob_tileset.Spike(725, 125))
    server.tiles.append(ob_tileset.Spike(775, 125))
    server.tiles.append(ob_tileset.RandomBox(575, 325))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_50X50, 1025, 325))
    server.tiles.append(ob_tileset.Spike(975, 325, POS.LEFT))
    server.tiles.append(ob_tileset.Spike(1025, 275, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(1075, 325, POS.RIGHT))
    server.tiles.append(ob_tileset.Spike(1025, 375))

    object_manager.add_objects(server.tiles, object_manager.OL_TILESET)

    # Interactives
    server.interactives.append(ob_interactive.WireMesh(625, 1325, 1275, 225))
    object_manager.add_objects(server.interactives, L.INTERACTIVES)

    # Foreground
    server.foreground = []
    object_manager.add_objects(server.foreground, L.FOREGROUND)

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
