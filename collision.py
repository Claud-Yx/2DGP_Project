import ob_player
import ob_tileset
import ob_enemy
import ob_background

import object_manager

from value import *

import game_object


def collide(a: (0, 0, 0, 0), b: (0, 0, 0, 0)):
    left_a, bottom_a, right_a, top_a = a
    left_b, bottom_b, right_b, top_b = b

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def collide_objects(obj: object, obj_m: object_manager):
    if (obj.__class__ == ob_background.Background or
        not obj_m.__name__ == object_manager.

    ):
        return

    if obj.__class__ == ob_player.Player:
        collide_player_to_tiles(obj1, obj2)


def collide_player_to_tiles(player: ob_player.Player, tiles: List[ob_tileset.TileSet]):
    for tile in tiles:
        if (player.get_bb_on(HB.STAND) and tile.get_bb_on(HB.COLLISION_BODY) and
                collide(player.get_bb(HB.STAND),
                        tile.get_bb(HB.COLLISION_BODY)
                        )
        ):
            player.jump_power = 0
            player.on_floor = True
            player.is_fall = False
            player.is_jump = False

            if (player.get_bb(HB.STAND)[POS.BOTTOM] < tile.get_bb(HB.COLLISION_BODY)[POS.TOP] and
                    player.action != ACTION.JUMP):
                player.y = (
                        player.bounding_box[HB.STAND].range[POS.BOTTOM] +
                        tile.get_bb(HB.COLLISION_BODY)[POS.TOP]
                )

            break
        elif (player.get_bb_on(HB.STAND) and tile.get_bb_on(HB.COLLISION_BODY) and
              not collide(
                  player.get_bb(HB.STAND),
                  tile.get_bb(HB.COLLISION_BODY)
              )
        ):
            player.on_floor = False

    for tile in tiles:
        if (player.get_bb_on(HB.COLLISION_BODY) and
                tile.get_bb_on(HB.COLLISION_BODY) and
                collide(player.get_bb(HB.COLLISION_BODY),
                        tile.get_bb(HB.COLLISION_BODY)
                        ) and
                player.get_bb(HB.COLLISION_BODY)[POS.BOTTOM] < tile.get_bb(HB.COLLISION_BODY)[POS.TOP]
        ):

            # ceiling
            if (tile.get_bb(HB.COLLISION_BODY)[POS.BOTTOM] <=
                    player.get_bb(HB.COLLISION_BODY)[POS.TOP] <=
                    tile.get_bb(HB.COLLISION_BODY)[POS.TOP] and
                    tile.get_bb(HB.COLLISION_BODY)[POS.LEFT] <=
                    player.get_bb(HB.COLLISION_BODY)[POS.RIGHT] <=
                    tile.get_bb(HB.COLLISION_BODY)[POS.RIGHT] and
                    tile.get_bb(HB.COLLISION_BODY)[POS.LEFT] <=
                    player.get_bb(HB.COLLISION_BODY)[POS.LEFT] <=
                    tile.get_bb(HB.COLLISION_BODY)[POS.RIGHT]
            ):
                player.jump_power = 0
                player.y = (
                        tile.get_bb(HB.COLLISION_BODY)[POS.BOTTOM] -
                        player.get_bb_range(HB.COLLISION_BODY)[POS.TOP]
                )

            else:
                # left wall
                if (tile.get_bb(HB.COLLISION_BODY)[POS.RIGHT] >=
                        player.get_bb(HB.COLLISION_BODY)[POS.RIGHT] >=
                        tile.get_bb(HB.COLLISION_BODY)[POS.LEFT]
                ):
                    if player.facing == DIR.LEFT:
                        player.velocity = 0
                    player.x = (
                            tile.get_bb(HB.COLLISION_BODY)[POS.LEFT] -
                            player.get_bb_range(HB.COLLISION_BODY)[POS.RIGHT]
                    )

                # right wall
                if (tile.get_bb(HB.COLLISION_BODY)[POS.LEFT] <=
                        player.get_bb(HB.COLLISION_BODY)[POS.LEFT] <=
                        tile.get_bb(HB.COLLISION_BODY)[POS.RIGHT]
                ):
                    if player.facing == DIR.RIGHT:
                        player.velocity = 0
                    player.x = (
                            tile.get_bb(HB.COLLISION_BODY)[POS.RIGHT] +
                            player.get_bb_range(HB.COLLISION_BODY)[POS.LEFT]
                    )


def collide_enemies_to_tiles(enemies, tiles):
    for enemy in enemies:
        for tile in tiles:
            if (enemy.get_bb_on(HB.STAND) and tile.get_bb_on(HB.COLLISION_BODY) and
                    collide(enemy.get_bb(HB.STAND),
                            tile.get_bb(HB.COLLISION_BODY)
                            )
            ):
                enemy.jump_power = 0
                enemy.is_fall = False

                if (enemy.get_bb(HB.STAND)[POS.BOTTOM] < tile.get_bb(HB.COLLISION_BODY)[POS.TOP] and
                        enemy.action != ACTION.JUMP):
                    enemy.y = (
                            enemy.bounding_box[HB.STAND].range[POS.BOTTOM] +
                            tile.get_bb(HB.COLLISION_BODY)[POS.TOP]
                    )

                break
            elif (enemy.get_bb_on(HB.STAND) and tile.get_bb_on(HB.COLLISION_BODY) and
                  not collide(
                      enemy.get_bb(HB.STAND),
                      tile.get_bb(HB.COLLISION_BODY)
                  )
            ):
                enemy.is_fall = True

        for tile in tiles:
            if (enemy.get_bb_on(HB.COLLISION_BODY) and
                    tile.get_bb_on(HB.COLLISION_BODY) and
                    collide(enemy.get_bb(HB.COLLISION_BODY),
                            tile.get_bb(HB.COLLISION_BODY)
                            ) and
                    enemy.get_bb(HB.COLLISION_BODY)[POS.BOTTOM] < tile.get_bb(HB.COLLISION_BODY)[POS.TOP]
            ):

                # ceiling
                if (tile.get_bb(HB.COLLISION_BODY)[POS.BOTTOM] <=
                        enemy.get_bb(HB.COLLISION_BODY)[POS.TOP] <=
                        tile.get_bb(HB.COLLISION_BODY)[POS.TOP] and
                        tile.get_bb(HB.COLLISION_BODY)[POS.LEFT] <=
                        enemy.get_bb(HB.COLLISION_BODY)[POS.RIGHT] <=
                        tile.get_bb(HB.COLLISION_BODY)[POS.RIGHT] and
                        tile.get_bb(HB.COLLISION_BODY)[POS.LEFT] <=
                        enemy.get_bb(HB.COLLISION_BODY)[POS.LEFT] <=
                        tile.get_bb(HB.COLLISION_BODY)[POS.RIGHT]
                ):
                    enemy.jump_power = 0
                    enemy.y = (
                            tile.get_bb(HB.COLLISION_BODY)[POS.BOTTOM] -
                            enemy.get_bb_range(HB.COLLISION_BODY)[POS.TOP]
                    )

                else:
                    # left wall
                    if (tile.get_bb(HB.COLLISION_BODY)[POS.RIGHT] >=
                            enemy.get_bb(HB.COLLISION_BODY)[POS.RIGHT] >=
                            tile.get_bb(HB.COLLISION_BODY)[POS.LEFT]
                    ):
                        print("left")
                        enemy.x_direction = DIR.LEFT
                        enemy.facing = enemy.x_direction
                        enemy.set_info()
                        enemy.x = (
                                tile.get_bb(HB.COLLISION_BODY)[POS.LEFT] -
                                enemy.get_bb_range(HB.COLLISION_BODY)[POS.RIGHT]
                        )

                    # right wall
                    if (tile.get_bb(HB.COLLISION_BODY)[POS.LEFT] <=
                            enemy.get_bb(HB.COLLISION_BODY)[POS.LEFT] <=
                            tile.get_bb(HB.COLLISION_BODY)[POS.RIGHT]
                    ):
                        print("right")
                        enemy.x_direction = DIR.RIGHT
                        enemy.facing = enemy.x_direction
                        enemy.set_info()
                        enemy.x = (
                                tile.get_bb(HB.COLLISION_BODY)[POS.RIGHT] +
                                enemy.get_bb_range(HB.COLLISION_BODY)[POS.LEFT]
                        )
