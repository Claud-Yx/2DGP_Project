import ob_interactive
import ob_item
import ob_player
import ob_tileset
import ob_enemy

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
            player.ay = (player.get_bb_range(HB.BOTTOM)[POS.BOTTOM] +
                         tile.get_bb(HB.TOP)[POS.TOP])

        if isinstance(tile, ob_tileset.Spike) and not player.is_invincible and not player.is_star_power:
            player.is_damaged = True

        if player.cur_state == ob_player.ClimbState and player.on_wire_mesh is not None:
            player.on_wire_mesh.got_player = False

        return True

    else:
        player.on_floor = False
        return False


def collide_player_to_ceiling(player: ob_player.Player, tile: ob_tileset.TileSet) -> bool:
    if collide(player.get_bb(HB.TOP), tile.get_bb(HB.BOTTOM)):
        if not player.cur_state == ob_player.ClimbState:
            player.jump_power = 0

        if player.get_bb(HB.TOP)[POS.TOP] > tile.get_bb(HB.BOTTOM)[POS.BOTTOM]:
            ptop = player.get_bb_range(HB.TOP)[POS.TOP]
            if ptop < 0:
                ptop = abs(ptop)

            player.ay = (tile.get_bb(HB.BOTTOM)[POS.BOTTOM] -
                         ptop)

        tile: ob_tileset.RandomBox
        if tile.type_id == TID.RANDOM_BOX and not tile.is_empty and player.cur_state != ob_player.ClimbState:
            tile.is_hit = True

        tile: ob_tileset.Brick
        if tile.type_id == TID.BREAKABLE_BRICK and player.cur_state != ob_player.ClimbState:
            tile.hit_by = player.type_id

        if isinstance(tile, ob_tileset.Spike) and not player.is_invincible and not player.is_star_power:
            player.is_damaged = True

        elif (isinstance(tile, ob_tileset.RandomBox) or
              isinstance(tile, ob_tileset.Brick)) and player.cur_state != ob_player.ClimbState:
            if tile.on_enemy is not None:
                tile.on_enemy.dead_type = ACTION.DIE_B

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
            player.ax = (player.get_bb_range(HB.LEFT)[POS.LEFT] +
                         tile.get_bb(HB.RIGHT)[POS.RIGHT])

        if isinstance(tile, ob_tileset.Spike) and not player.is_invincible and not player.is_star_power:
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
            player.ax = (tile.get_bb(HB.LEFT)[POS.LEFT] -
                         player.get_bb_range(HB.RIGHT)[POS.RIGHT])

        if isinstance(tile, ob_tileset.Spike) and not player.is_invincible and not player.is_star_power:
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

        if enemy.get_bb(HB.BOTTOM)[POS.BOTTOM] < floor.get_bb(HB.TOP)[POS.TOP]:
            enemy.ay = (enemy.get_bb_range(HB.BOTTOM)[POS.BOTTOM] +
                        floor.get_bb(HB.TOP)[POS.TOP])

        if (isinstance(floor, ob_tileset.RandomBox) or
            isinstance(floor, ob_tileset.Brick)
        ):
            floor.on_enemy = enemy
            return False

        return True

    else:
        if (isinstance(floor, ob_tileset.RandomBox) or
            isinstance(floor, ob_tileset.Brick)
        ):
            floor.on_enemy = None

        enemy.is_fall = True
        return False


def check_enemy_to_cliff(enemy: ob_enemy, floor: ob_tileset) -> bool:
    if enemy.on_floor:
        if collide(enemy.get_bb(HB.CLIFF_CHECK), floor.get_bb(HB.TOP)):
            return False
        return True
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
            enemy.ax = (tile.get_bb(HB.LEFT)[POS.LEFT] -
                        enemy.get_bb_range(HB.RIGHT)[POS.RIGHT])
        elif (tile.get_bb(HB.LEFT)[POS.LEFT] <=
              enemy.get_bb(HB.LEFT)[POS.LEFT] <
              tile.get_bb(HB.RIGHT)[POS.RIGHT]
        ):
            enemy.ax = (tile.get_bb(HB.RIGHT)[POS.RIGHT] +
                        enemy.get_bb_range(HB.LEFT)[POS.LEFT])

        return True
    return False


def stomp_player_to_enemy(player: ob_player.Player, enemy: ob_enemy) -> bool:
    if isinstance(enemy, ob_enemy.Boo):
        return False
    if (collide(player.get_bb(HB.BOTTOM), enemy.get_bb(HB.TOP)) and
            not player.is_jump and not player.is_star_power):
        enemy.dead_type = ACTION.DIE_A

        # player
        player.is_fall = False
        player.is_jump = True
        if player.pressed_key_jump:
            player.jump_power = ob_player.MAX_JUMP_POWER + ob_player.JUMP_BOOST_TWO
            player.additional_jump_power = ob_player.MAX_JUMP_POWER + ob_player.JUMP_BOOST_TWO
        else:
            player.jump_power = get_pps_from_mps(10)
        player.ay = (player.get_bb_range(HB.BOTTOM)[POS.BOTTOM] + enemy.get_bb(HB.TOP)[POS.TOP]) + 1
        player.set_info(ACTION.JUMP)
        # enemy.switch_bb_all()

        return True
    return False


def hit_enemy_to_player(player: ob_player.Player, enemy: ob_enemy) -> bool:
    # Enemy collides to player
    if collide(player.get_bb(HB.BODY), enemy.get_bb(HB.BODY)):
        if player.is_star_power:
            enemy.dead_type = ACTION.DIE_B
        elif not player.is_invincible:
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

        if item.get_bb(HB.BOTTOM)[POS.BOTTOM] < floor.get_bb(HB.TOP)[POS.TOP]:
            item.ay = (item.get_bb_range(HB.BOTTOM)[POS.BOTTOM] +
                       floor.get_bb(HB.TOP)[POS.TOP]) + 1

        if item.type_id == TID.SUPER_STAR:
            item.is_jump = True

        return True
    else:
        item.is_fall = True
        return False


def collide_item_to_ceiling(item: ob_item.PowerUp, tile: ob_tileset.TileSet) -> bool:
    if collide(item.get_bb(HB.TOP), tile.get_bb(HB.BOTTOM)):
        if tile.__class__ == ob_tileset.RandomBox and tile.state == ob_tileset.RS.INVISIBLE:
            return False

        item.jump_power = 0
        item.is_jump = False

        if item.get_bb(HB.TOP)[POS.TOP] > tile.get_bb(HB.BOTTOM)[POS.BOTTOM]:
            ptop = item.get_bb_range(HB.TOP)[POS.TOP]
            if ptop < 0:
                ptop = abs(ptop) - 1

            item.ay = (tile.get_bb(HB.BOTTOM)[POS.BOTTOM] -
                       ptop) - 1

        return True

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
            item.ax = (tile.get_bb(HB.LEFT)[POS.LEFT] -
                       item.get_bb_range(HB.RIGHT)[POS.RIGHT])
        elif (tile.get_bb(HB.LEFT)[POS.LEFT] <=
              item.get_bb(HB.LEFT)[POS.LEFT] <
              tile.get_bb(HB.RIGHT)[POS.RIGHT]
        ):
            item.ax = (tile.get_bb(HB.RIGHT)[POS.RIGHT] +
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
            if (itr.get_bb(HB.BODY)[POS.LEFT] - player.get_bb_range(HB.BODY)[POS.RIGHT] <=
                    player.ax <=
                    itr.get_bb(HB.BODY)[POS.RIGHT] + player.get_bb_range(HB.BODY)[POS.LEFT] and
                itr.get_bb(HB.BODY)[POS.BOTTOM] - player.get_bb_range(HB.BODY)[POS.TOP] <=
                    player.ay <=
                    itr.get_bb(HB.BODY)[POS.TOP]
            ):
                player.on_wire_mesh = itr
        return True

    else:
        if isinstance(itr, ob_interactive.WireMesh) and not player.is_damaged:
            itr.got_player = False
            player.on_wire_mesh = None
        return False
