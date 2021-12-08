import gs_framework
import ob_background
import ob_enemy
import ob_foreground
import ob_interactive
import ob_item
import ob_map
import ob_player
import ob_tileset
from ob_tileset import RS
import object_manager
import server
from value import *


def create_map():
    # Initialization:
    server.init()
    object_manager.objects = [[], [], [], [], []]

    # stage map
    server.stage = ob_map.Map(0, 0,
                              1200,
                              4000
                              )

    # background
    server.background = ob_background.Background()
    object_manager.add_object(server.background, L.BACKGROUND)

    # player
    server.player = ob_player.Player(TID.MARIO_SUPER, 11, 71)
    object_manager.add_object(server.player, object_manager.OL_CHARACTER)

    # item
    for y in range(64, 70):
        server.items.append(ob_item.Coin(11, y))
        server.items.append(ob_item.Coin(12, y))

    for x in range(3, 5):
        server.items.append(ob_item.Coin(x, 48))
        server.items.append(ob_item.Coin(x + 16, 48))
        server.items.append(ob_item.Coin(x, 47))
        server.items.append(ob_item.Coin(x + 16, 47))

    for x in [16, 20]:
        for y in [36, 37, 39, 40]:
            server.items.append(ob_item.Coin(x, y))

    for y in range(37, 40):
        server.items.append(ob_item.Coin(18, y))

    for x in range(14, 22):
        for y in range(21, 27):
            server.items.append(ob_item.Coin(x, y))

    server.items.append(ob_item.Coin(11, 15))
    server.items.append(ob_item.Coin(12, 15))
    server.items.append(ob_item.Coin(11, 14))
    server.items.append(ob_item.Coin(12, 14))



    object_manager.add_objects(server.items, L.ITEMS)

    # enemy
    # server.enemies.append(ob_enemy.Boo(0, 77))
    # server.enemies.append(ob_enemy.Boo(24, 65))
    # server.enemies.append(ob_enemy.Boo(0, 59))
    # server.enemies.append(ob_enemy.Boo(24, 53))

    server.enemies.append(ob_enemy.Goomba(2, 46))
    server.enemies.append(ob_enemy.Goomba(21, 46, DIR.LEFT))

    server.enemies.append(ob_enemy.DryBones(11, 44))
    server.enemies.append(ob_enemy.DryBones(14, 28))
    server.enemies.append(ob_enemy.DryBones(2, 24))
    server.enemies.append(ob_enemy.DryBones(4, 22))
    server.enemies.append(ob_enemy.DryBones(6, 20))
    server.enemies.append(ob_enemy.DryBones(19, 5))
    server.enemies.append(ob_enemy.DryBones(19, 2))

    object_manager.add_objects(server.enemies, L.ENEMIES)

    # tile sets
    for x in range(4, 20, 2):
        server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, x, 0))

    for y in range(0, 80, 2):
        server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 0, y))
        server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 22, y))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 10, 70))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 12, 70))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 5, 66))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 17, 66))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 11, 55))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 11, 57))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 11, 59))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 11, 61))

    for x in range(3, 10):
        server.tiles.append(ob_tileset.Brick(x, 58))

    for x in range(14, 21):
        server.tiles.append(ob_tileset.Brick(x, 58))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 5, 50))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 17, 50))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 2, 44))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 4, 44))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 6, 44))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 8, 44))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 14, 44))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 16, 44))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 18, 44))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 20, 44))

    server.tiles.append(ob_tileset.RandomBox(11, 43, item=TID.SUPER_MUSHROOM))
    server.tiles.append(ob_tileset.RandomBox(12, 43))

    server.tiles.append(ob_tileset.RandomBox(21, 42, item=TID.LIFE_MUSHROOM))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 10, 39))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 12, 39))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 10, 37))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 12, 37))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 10, 35))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 12, 35))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 10, 33))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 12, 33))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_50X50, 3, 34))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_50X50, 7, 32))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_50X50, 3, 29))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 17, 28))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 14, 27))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 16, 27))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 6, 18))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 4, 20))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 2, 22))

    for x in range(14, 22):
        server.tiles.append(ob_tileset.RandomBox(x, 20, state=RS.POLYMORPH))

    for y in range(18, 28, 2):
        server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_50X100, 13, y))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 2, 17))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 4, 17))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 6, 17))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 8, 17))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_50X50, 12, 17))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 13, 17))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 15, 17))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 17, 17))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 19, 17))

    server.tiles.append(ob_tileset.RandomBox(2, 12, state=RS.INVISIBLE))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 11, 12))
    for x in range(13, 22):
        server.tiles.append(ob_tileset.RandomBox(x, 12, state=RS.INVISIBLE))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 18, 9))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 20, 9))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 5, 7))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 3, 7))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_50X100, 2, 7))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 7, 7))

    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 13, 5))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 15, 5))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 17, 5))

    server.tiles.append(ob_tileset.RandomBox(19, 4, item=TID.SUPER_MUSHROOM))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X50, 20, 4))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_50X50, 11, 4))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_50X50, 9, 2))
    server.tiles.append(ob_tileset.TileSet(TID.CASTLE_BLOCK_100X100, 10, 2))

    server.tiles.append(ob_tileset.Spike(5, 68))
    server.tiles.append(ob_tileset.Spike(6, 68))
    server.tiles.append(ob_tileset.Spike(17, 68))
    server.tiles.append(ob_tileset.Spike(18, 68))

    server.tiles.append(ob_tileset.Spike(4, 67, POS.LEFT))
    server.tiles.append(ob_tileset.Spike(7, 67, POS.RIGHT))
    server.tiles.append(ob_tileset.Spike(16, 67, POS.LEFT))
    server.tiles.append(ob_tileset.Spike(19, 67, POS.RIGHT))

    server.tiles.append(ob_tileset.Spike(4, 66, POS.LEFT))
    server.tiles.append(ob_tileset.Spike(7, 66, POS.RIGHT))
    server.tiles.append(ob_tileset.Spike(16, 66, POS.LEFT))
    server.tiles.append(ob_tileset.Spike(19, 66, POS.RIGHT))

    server.tiles.append(ob_tileset.Spike(5, 65, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(6, 65, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(17, 65, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(18, 65, POS.BOTTOM))

    server.tiles.append(ob_tileset.Spike(11, 63))
    server.tiles.append(ob_tileset.Spike(12, 63))

    for y in range(55, 63):
        server.tiles.append(ob_tileset.Spike(10, y, POS.LEFT))
        server.tiles.append(ob_tileset.Spike(13, y, POS.RIGHT))

    server.tiles.append(ob_tileset.Spike(11, 54, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(12, 54, POS.BOTTOM))

    server.tiles.append(ob_tileset.Spike(5, 52))
    server.tiles.append(ob_tileset.Spike(6, 52))
    server.tiles.append(ob_tileset.Spike(17, 52))
    server.tiles.append(ob_tileset.Spike(18, 52))

    server.tiles.append(ob_tileset.Spike(4, 51, POS.LEFT))
    server.tiles.append(ob_tileset.Spike(7, 51, POS.RIGHT))
    server.tiles.append(ob_tileset.Spike(16, 51, POS.LEFT))
    server.tiles.append(ob_tileset.Spike(19, 51, POS.RIGHT))

    server.tiles.append(ob_tileset.Spike(4, 50, POS.LEFT))
    server.tiles.append(ob_tileset.Spike(7, 50, POS.RIGHT))
    server.tiles.append(ob_tileset.Spike(16, 50, POS.LEFT))
    server.tiles.append(ob_tileset.Spike(19, 50, POS.RIGHT))

    server.tiles.append(ob_tileset.Spike(5, 49, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(6, 49, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(17, 49, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(18, 49, POS.BOTTOM))

    for x in range(2, 10):
        server.tiles.append(ob_tileset.Spike(x, 45))
        server.tiles.append(ob_tileset.Spike(x + 12, 45))

    for y in range(33, 41):
        server.tiles.append(ob_tileset.Spike(9, y, POS.LEFT))
        server.tiles.append(ob_tileset.Spike(14, y, POS.RIGHT))

    server.tiles.append(ob_tileset.Spike(13, 28))

    for y in range(18, 28):
        server.tiles.append(ob_tileset.Spike(12, y, POS.LEFT))

    server.tiles.append(ob_tileset.Spike(11, 13))
    server.tiles.append(ob_tileset.Spike(12, 13))

    server.tiles.append(ob_tileset.Spike(18, 8, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(19, 8, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(20, 8, POS.BOTTOM))
    server.tiles.append(ob_tileset.Spike(21, 7, POS.BOTTOM))

    object_manager.add_objects(server.tiles, object_manager.OL_TILESET)

    # Interactives

    server.interactives.append(ob_interactive.WireMesh(14, 70, 21, 59, dst_x=-12))
    server.interactives.append(ob_interactive.WireMesh(2, 57, 9, 46, dst_x=12))
    server.interactives.append(ob_interactive.WireMesh(2, 39, 13, 35))
    server.interactives.append(ob_interactive.WireMesh(2, 27, 5, 25))
    server.interactives.append(ob_interactive.WireMesh(2, 16, 7, 13))
    object_manager.add_objects(server.interactives, L.INTERACTIVES)

    # Foreground
    server.foreground = []
    for y in range(-1, 81, 2):
        server.foreground.append(ob_foreground.Foreground(-2, y, TN.TILESETS, TID.CASTLE_BLOCK_100X100))
        server.foreground.append(ob_foreground.Foreground(24, y, TN.TILESETS, TID.CASTLE_BLOCK_100X100))

    object_manager.add_objects(server.foreground, L.FOREGROUND)
