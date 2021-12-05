import ob_interactive
import ob_item
import ob_player
import ob_tileset
import ob_enemy
import ob_background

import object_manager

from value import *

import game_object


def collide(a: (0, 0, 0, 0), b: (0, 0, 0, 0)):
    if a == (-1, -1, -1, -1) or b == (-1, -1, -1, -1):
        return False

    left_a, bottom_a, right_a, top_a = a
    left_b, bottom_b, right_b, top_b = b

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


# def collide_objects(obj: object, obj_m: object_manager):
#     if (obj.__class__ == ob_background.Background or
#         not obj_m.__name__ == object_manager.
#
#     ):
#         return
#
#     if obj.__class__ == ob_player.Player:
#         collide_player_to_tiles(obj1, obj2)


def collide_player_to_floor(player: ob_player.Player, tile: ob_tileset.TileSet) -> bool:
    if collide(player.get_bb(HB.BOTTOM), tile.get_bb(HB.TOP)):

        if tile.__class__ == ob_tileset.RandomBox and tile.state == ob_tileset.RS.INVISIBLE:
            return False

        player.jump_power = 0
        player.on_floor = True
        player.is_fall = False
        player.is_jump = False

        if (player.get_bb(HB.BOTTOM)[POS.BOTTOM] < tile.get_bb(HB.TOP)[POS.TOP] and
                player.action != ACTION.JUMP
        ):
            player.y = (player.get_bb_range(HB.BOTTOM)[POS.BOTTOM] +
                        tile.get_bb(HB.TOP)[POS.TOP])

        if isinstance(tile, ob_tileset.Spike) and not player.is_invincible:
            player.is_damaged = True

        return True

    else:
        player.on_floor = False
        return False


def collide_player_to_ceiling(player: ob_player.Player, tile: ob_tileset.TileSet) -> bool:
    if collide(player.get_bb(HB.TOP), tile.get_bb(HB.BOTTOM)):
        player.jump_power = 0

        if player.get_bb(HB.TOP)[POS.TOP] > tile.get_bb(HB.BOTTOM)[POS.BOTTOM]:
            ptop = player.get_bb_range(HB.TOP)[POS.TOP]
            if ptop < 0:
                ptop = abs(ptop)

            player.y = (tile.get_bb(HB.BOTTOM)[POS.BOTTOM] -
                        ptop)

        tile: ob_tileset.RandomBox
        if tile.type_id == TID.RANDOM_BOX and not tile.is_empty:
            tile.is_hit = True

        tile: ob_tileset.Brick
        if tile.type_id == TID.BREAKABLE_BRICK:
            tile.hit_by = player.type_id

        # if tile.type_id == TID.RANDOM_BOX or tile.type_id == TID.BREAKABLE_BRICK:
        #     return False

        if isinstance(tile, ob_tileset.Spike) and not player.is_invincible:
            player.is_damaged = True

        return False

    return False


def collide_player_to_right_wall(player: ob_player.Player, tile: ob_tileset.TileSet) -> bool:
    if (collide(player.get_bb(HB.LEFT), tile.get_bb(HB.BODY)) and
            player.get_bb(HB.BOTTOM)[POS.BOTTOM] < tile.get_bb(HB.TOP)[POS.TOP]
    ):

        if tile.__class__ == ob_tileset.RandomBox and tile.state == ob_tileset.RS.INVISIBLE:
            return False

        player.velocity = 0
        player.is_stuck_left = True

        if player.get_bb(HB.LEFT)[POS.LEFT] < tile.get_bb(HB.RIGHT)[POS.RIGHT]:
            player.x = (player.get_bb_range(HB.LEFT)[POS.LEFT] +
                        tile.get_bb(HB.RIGHT)[POS.RIGHT])

        if isinstance(tile, ob_tileset.Spike) and not player.is_invincible:
            player.is_damaged = True

        return True

    else:
        player.is_stuck_left = False
        return False


def collide_player_to_left_wall(player: ob_player.Player, tile: ob_tileset.TileSet) -> bool:
    if (collide(player.get_bb(HB.RIGHT), tile.get_bb(HB.BODY)) and
            player.get_bb(HB.BOTTOM)[POS.BOTTOM] < tile.get_bb(HB.TOP)[POS.TOP]
    ):

        if tile.__class__ == ob_tileset.RandomBox and tile.state == ob_tileset.RS.INVISIBLE:
            return False

        player.velocity = 0
        player.is_stuck_right = True

        if player.get_bb(HB.RIGHT)[POS.RIGHT] > tile.get_bb(HB.LEFT)[POS.LEFT]:
            player.x = (tile.get_bb(HB.LEFT)[POS.LEFT] -
                        player.get_bb_range(HB.RIGHT)[POS.RIGHT])

        if isinstance(tile, ob_tileset.Spike) and not player.is_invincible:
            player.is_damaged = True

        return True

    else:
        player.is_stuck_right = False
        return False


def collide_enemy_to_floor(enemy: ob_enemy, floor: ob_tileset.TileSet) -> bool:
    if collide(enemy.get_bb(HB.BOTTOM), floor.get_bb(HB.TOP)):

        if floor.__class__ == ob_tileset.RandomBox and floor.state == ob_tileset.RS.INVISIBLE:
            return False

        enemy.jump_power = 0
        enemy.is_fall = False
        enemy.on_floor = True

        # print("enemy.action: " + str(enemy.action) +
        #       "enemy.pos: " + str(enemy.x) + ", " + str(enemy.y))
        # print("enemy.bottom: " + str(enemy.get_bb(HB.BOTTOM)[POS.BOTTOM]) + " / floor.top: " +
        #       str(floor.get_bb(HB.TOP)[POS.TOP]))
        if enemy.get_bb(HB.BOTTOM)[POS.BOTTOM] < floor.get_bb(HB.TOP)[POS.TOP]:
            # print("enemy.bb_range.bottom: " + str(enemy.get_bb_range(HB.BOTTOM)))
            # print("enemy.get_bb_range.bottom: " + str(enemy.get_bb_range(HB.BOTTOM)[HB.BOTTOM]) +
            #       " / floor.get_bb.top: " + str(floor.get_bb(HB.TOP)[HB.TOP]) +
            #       " / sum: " + str(enemy.get_bb_range(HB.BOTTOM)[HB.BOTTOM] + floor.get_bb(HB.TOP)[HB.TOP]))
            enemy.y = (enemy.get_bb_range(HB.BOTTOM)[POS.BOTTOM] +
                       floor.get_bb(HB.TOP)[POS.TOP]) + 1

        return True
    else:
        enemy.is_fall = True
        return False


def collide_enemy_to_wall(enemy: ob_enemy, tile: ob_tileset.TileSet) -> bool:
    if ((collide(enemy.get_bb(HB.RIGHT), tile.get_bb(HB.BODY)) or
         collide(enemy.get_bb(HB.LEFT), tile.get_bb(HB.BODY))) and
            enemy.get_bb(HB.BOTTOM)[POS.BOTTOM] < tile.get_bb(HB.TOP)[POS.TOP]
    ):

        if tile.__class__ == ob_tileset.RandomBox and tile.state == ob_tileset.RS.INVISIBLE:
            return False

        enemy.x_direction *= -1
        enemy.facing = enemy.x_direction
        enemy.set_info()

        if (tile.get_bb(HB.RIGHT)[POS.RIGHT] >=
                enemy.get_bb(HB.RIGHT)[POS.RIGHT] >
                tile.get_bb(HB.LEFT)[POS.LEFT]
        ):
            enemy.x = (tile.get_bb(HB.LEFT)[POS.LEFT] -
                       enemy.get_bb_range(HB.RIGHT)[POS.RIGHT])
        elif (tile.get_bb(HB.LEFT)[POS.LEFT] <=
              enemy.get_bb(HB.LEFT)[POS.LEFT] <
              tile.get_bb(HB.RIGHT)[POS.RIGHT]
        ):
            enemy.x = (tile.get_bb(HB.RIGHT)[POS.RIGHT] +
                       enemy.get_bb_range(HB.LEFT)[POS.LEFT])

        return True
    return False


def stomp_player_to_enemy(player: ob_player.Player, enemy: ob_enemy) -> bool:
    # print("player.bb_bottom pos: %d / enemy.bb_top pos: %d" %
    #       (player.get_bb(HB.BOTTOM)[POS.BOTTOM], enemy.get_bb(HB.TOP)[POS.TOP]))
    # Player stomps enemy
    if collide(player.get_bb(HB.BOTTOM), enemy.get_bb(HB.TOP)) and not player.is_jump:
        enemy.is_dead = True

        # player
        player.is_fall = False
        player.is_jump = True
        if player.pressed_key_jump:
            player.jump_power = ob_player.MAX_JUMP_POWER + ob_player.JUMP_BOOST_TWO
            player.additional_jump_power = ob_player.MAX_JUMP_POWER + ob_player.JUMP_BOOST_TWO
        else:
            player.jump_power = get_pps_from_mps(10)
        player.y = (player.get_bb_range(HB.BOTTOM)[POS.BOTTOM] + enemy.get_bb(HB.TOP)[POS.TOP]) + 1
        player.set_info(ACTION.JUMP)
        enemy.switch_bb_all()

        return True
    return False


def hit_enemy_to_player(player: ob_player.Player, enemy: ob_enemy) -> bool:
    # Enemy collides to player
    if collide(player.get_bb(HB.BODY), enemy.get_bb(HB.BODY)) and not player.is_invincible:
        player.is_damaged = True
        return True
    return False


def collide_item_to_floor(item: ob_item.Item, floor: ob_tileset.TileSet) -> bool:
    if collide(item.get_bb(HB.BOTTOM), floor.get_bb(HB.TOP)):

        if floor.__class__ == ob_tileset.RandomBox and floor.state == ob_tileset.RS.INVISIBLE:
            return False

        item.jump_power = 0
        item.is_fall = False
        item.on_floor = True

        # print("enemy.action: " + str(enemy.action) +
        #       "enemy.pos: " + str(enemy.x) + ", " + str(enemy.y))
        # print("enemy.bottom: " + str(enemy.get_bb(HB.BOTTOM)[POS.BOTTOM]) + " / floor.top: " +
        #       str(floor.get_bb(HB.TOP)[POS.TOP]))
        if item.get_bb(HB.BOTTOM)[POS.BOTTOM] < floor.get_bb(HB.TOP)[POS.TOP]:
            # print("enemy.bb_range.bottom: " + str(enemy.get_bb_range(HB.BOTTOM)))
            # print("enemy.get_bb_range.bottom: " + str(enemy.get_bb_range(HB.BOTTOM)[HB.BOTTOM]) +
            #       " / floor.get_bb.top: " + str(floor.get_bb(HB.TOP)[HB.TOP]) +
            #       " / sum: " + str(enemy.get_bb_range(HB.BOTTOM)[HB.BOTTOM] + floor.get_bb(HB.TOP)[HB.TOP]))
            item.y = (item.get_bb_range(HB.BOTTOM)[POS.BOTTOM] +
                      floor.get_bb(HB.TOP)[POS.TOP]) + 1

        return True
    else:
        item.is_fall = True
        return False


def collide_item_to_wall(item: ob_item.Item, tile: ob_tileset.TileSet) -> bool:
    if ((collide(item.get_bb(HB.RIGHT), tile.get_bb(HB.BODY)) or
         collide(item.get_bb(HB.LEFT), tile.get_bb(HB.BODY))) and
            item.get_bb(HB.BOTTOM)[POS.BOTTOM] < tile.get_bb(HB.TOP)[POS.TOP]
    ):

        if tile.__class__ == ob_tileset.RandomBox and tile.state == ob_tileset.RS.INVISIBLE:
            return False

        item.x_direction *= -1
        item.facing = item.x_direction
        item.set_info()

        if (tile.get_bb(HB.RIGHT)[POS.RIGHT] >=
                item.get_bb(HB.RIGHT)[POS.RIGHT] >
                tile.get_bb(HB.LEFT)[POS.LEFT]
        ):
            item.x = (tile.get_bb(HB.LEFT)[POS.LEFT] -
                      item.get_bb_range(HB.RIGHT)[POS.RIGHT])
        elif (tile.get_bb(HB.LEFT)[POS.LEFT] <=
              item.get_bb(HB.LEFT)[POS.LEFT] <
              tile.get_bb(HB.RIGHT)[POS.RIGHT]
        ):
            item.x = (tile.get_bb(HB.RIGHT)[POS.RIGHT] +
                      item.get_bb_range(HB.LEFT)[POS.LEFT])

        return True
    return False


def collide_item_to_player(player: ob_player.Player, item: ob_item.Item) -> bool:
    # Item collides to player
    if collide(player.get_bb(HB.BODY), item.get_bb(HB.BODY)):
        player.taken_item = (item.type_name, item.type_id)
        item.is_dead = True
        return True
    return False


def collide_player_to_interactive(player: ob_player.Player, itr: game_object.GameObject) -> bool:
    if collide(player.get_bb(HB.BODY), itr.get_bb(HB.BODY)):
        if isinstance(itr, ob_interactive.WireMesh):
            itr.got_player = True
            player.on_wire_mesh = itr

    else:
        if isinstance(itr, ob_interactive.WireMesh):
            itr.got_player = False
            player.on_wire_mesh = None
