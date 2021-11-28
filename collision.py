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
        player.jump_power = 0
        player.on_floor = True
        player.is_fall = False
        player.is_jump = False

        if (player.get_bb(HB.BOTTOM)[POS.BOTTOM] < tile.get_bb(HB.TOP)[POS.TOP] and
                player.action != ACTION.JUMP
        ):
            player.y = (player.get_bb_range(HB.BOTTOM)[POS.BOTTOM] +
                        tile.get_bb(HB.TOP)[POS.TOP])

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

        return True

    return False


def collide_player_to_right_wall(player: ob_player.Player, tile: ob_tileset.TileSet) -> bool:
    if (collide(player.get_bb(HB.LEFT), tile.get_bb(HB.BODY)) and
            player.get_bb(HB.BOTTOM)[POS.BOTTOM] < tile.get_bb(HB.TOP)[POS.TOP]
    ):
        player.velocity = 0
        player.is_stuck_left = True

        if player.get_bb(HB.LEFT)[POS.LEFT] < tile.get_bb(HB.RIGHT)[POS.RIGHT]:
            player.x = (player.get_bb_range(HB.LEFT)[POS.LEFT] +
                        tile.get_bb(HB.RIGHT)[POS.RIGHT])

        return True

    else:
        player.is_stuck_left = False
        return False


def collide_player_to_left_wall(player: ob_player.Player, tile: ob_tileset.TileSet) -> bool:
    if (collide(player.get_bb(HB.RIGHT), tile.get_bb(HB.BODY)) and
            player.get_bb(HB.BOTTOM)[POS.BOTTOM] < tile.get_bb(HB.TOP)[POS.TOP]
    ):
        player.velocity = 0
        player.is_stuck_right = True

        if player.get_bb(HB.RIGHT)[POS.RIGHT] > tile.get_bb(HB.LEFT)[POS.LEFT]:
            player.x = (tile.get_bb(HB.LEFT)[POS.LEFT] -
                        player.get_bb_range(HB.RIGHT)[POS.RIGHT])

        return True

    else:
        player.is_stuck_right = False
        return False


def collide_enemy_to_floor(enemy: ob_enemy, floor: ob_tileset.TileSet) -> bool:
    if collide(enemy.get_bb(HB.BOTTOM), floor.get_bb(HB.TOP)):
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
    if collide(player.get_bb(HB.BOTTOM), enemy.get_bb(HB.TOP)) and player.is_fall:
        enemy.is_dead = True

        # player
        player.is_fall = False
        player.is_jump = True
        if player.pressed_key_jump:
            player.jump_power = ob_player.MAX_JUMP_POWER + ob_player.JUMP_BOOST_ONE
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