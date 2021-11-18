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


def collide_player_to_tiles(player, tiles):
    for tile in tiles:
        if (player.get_bb_on(HB.STAND) and tile.get_bb_on(HB.COLLISION) and
                collide(player.get_bb(HB.STAND),
                        tile.get_bb(HB.COLLISION)
                        )
        ):
            player.jump_power = 0
            player.on_floor = True
            player.is_fall = False
            player.is_jump = False

            if (player.get_bb(HB.STAND)[POS.BOTTOM] < tile.get_bb(HB.COLLISION)[POS.TOP] and
                    player.action != ACTION.JUMP):
                player.y = (
                        player.bounding_box[HB.STAND].range[POS.BOTTOM] +
                        tile.get_bb(HB.COLLISION)[POS.TOP]
                )

            break
        elif (player.get_bb_on(HB.STAND) and tile.get_bb_on(HB.COLLISION) and
              not collide(
                  player.get_bb(HB.STAND),
                  tile.get_bb(HB.COLLISION)
              )
        ):
            player.on_floor = False

    for tile in tiles:
        if (player.get_bb_on(HB.COLLISION) and
                tile.get_bb_on(HB.COLLISION) and
                collide(player.get_bb(HB.COLLISION),
                        tile.get_bb(HB.COLLISION)
                        ) and
                player.get_bb(HB.COLLISION)[POS.BOTTOM] < tile.get_bb(HB.COLLISION)[POS.TOP]
        ):

            # ceiling
            if (tile.get_bb(HB.COLLISION)[POS.BOTTOM] <=
                    player.get_bb(HB.COLLISION)[POS.TOP] <=
                    tile.get_bb(HB.COLLISION)[POS.TOP] and
                    tile.get_bb(HB.COLLISION)[POS.LEFT] <=
                    player.get_bb(HB.COLLISION)[POS.RIGHT] <=
                    tile.get_bb(HB.COLLISION)[POS.RIGHT] and
                    tile.get_bb(HB.COLLISION)[POS.LEFT] <=
                    player.get_bb(HB.COLLISION)[POS.LEFT] <=
                    tile.get_bb(HB.COLLISION)[POS.RIGHT]
            ):
                player.jump_power = 0
                player.y = (
                        tile.get_bb(HB.COLLISION)[POS.BOTTOM] -
                        player.get_bb_range(HB.COLLISION)[POS.TOP]
                )

            else:
                # left wall
                if (tile.get_bb(HB.COLLISION)[POS.RIGHT] >=
                        player.get_bb(HB.COLLISION)[POS.RIGHT] >=
                        tile.get_bb(HB.COLLISION)[POS.LEFT]
                ):
                    if player.facing == game_object.D_LEFT:
                        player.velocity = 0
                    player.x = (
                            tile.get_bb(HB.COLLISION)[POS.LEFT] -
                            player.get_bb_range(HB.COLLISION)[POS.RIGHT]
                    )

                # right wall
                if (tile.get_bb(HB.COLLISION)[POS.LEFT] <=
                        player.get_bb(HB.COLLISION)[POS.LEFT] <=
                        tile.get_bb(HB.COLLISION)[POS.RIGHT]
                ):
                    if player.facing == game_object.D_RIGHT:
                        player.velocity = 0
                    player.x = (
                            tile.get_bb(HB.COLLISION)[POS.RIGHT] +
                            player.get_bb_range(HB.COLLISION)[POS.LEFT]
                    )

def collide_enemies_to_tiles(enemies, tiles):
    for enemy in enemies:
        for tile in tiles:
            if (enemy.get_bb_on(HB.STAND) and tile.get_bb_on(HB.COLLISION) and
                    collide(enemy.get_bb(HB.STAND),
                            tile.get_bb(HB.COLLISION)
                            )
            ):
                enemy.jump_power = 0
                enemy.is_fall = False

                if (enemy.get_bb(HB.STAND)[POS.BOTTOM] < tile.get_bb(HB.COLLISION)[POS.TOP] and
                        enemy.action != ACTION.JUMP):
                    enemy.y = (
                            enemy.bounding_box[HB.STAND].range[POS.BOTTOM] +
                            tile.get_bb(HB.COLLISION)[POS.TOP]
                    )

                break
            elif (enemy.get_bb_on(HB.STAND) and tile.get_bb_on(HB.COLLISION) and
                  not collide(
                      enemy.get_bb(HB.STAND),
                      tile.get_bb(HB.COLLISION)
                  )
            ):
                enemy.is_fall = True

        for tile in tiles:
            if (enemy.get_bb_on(HB.COLLISION) and
                    tile.get_bb_on(HB.COLLISION) and
                    collide(enemy.get_bb(HB.COLLISION),
                            tile.get_bb(HB.COLLISION)
                            ) and
                    enemy.get_bb(HB.COLLISION)[POS.BOTTOM] < tile.get_bb(HB.COLLISION)[POS.TOP]
            ):

                # ceiling
                if (tile.get_bb(HB.COLLISION)[POS.BOTTOM] <=
                        enemy.get_bb(HB.COLLISION)[POS.TOP] <=
                        tile.get_bb(HB.COLLISION)[POS.TOP] and
                        tile.get_bb(HB.COLLISION)[POS.LEFT] <=
                        enemy.get_bb(HB.COLLISION)[POS.RIGHT] <=
                        tile.get_bb(HB.COLLISION)[POS.RIGHT] and
                        tile.get_bb(HB.COLLISION)[POS.LEFT] <=
                        enemy.get_bb(HB.COLLISION)[POS.LEFT] <=
                        tile.get_bb(HB.COLLISION)[POS.RIGHT]
                ):
                    enemy.jump_power = 0
                    enemy.y = (
                            tile.get_bb(HB.COLLISION)[POS.BOTTOM] -
                            enemy.get_bb_range(HB.COLLISION)[POS.TOP]
                    )

                else:
                    # left wall
                    if (tile.get_bb(HB.COLLISION)[POS.RIGHT] >=
                            enemy.get_bb(HB.COLLISION)[POS.RIGHT] >=
                            tile.get_bb(HB.COLLISION)[POS.LEFT]
                    ):
                        print("left")
                        enemy.x_direction = game_object.D_LEFT
                        enemy.facing = enemy.x_direction
                        enemy.set_info()
                        enemy.x = (
                                tile.get_bb(HB.COLLISION)[POS.LEFT] -
                                enemy.get_bb_range(HB.COLLISION)[POS.RIGHT]
                        )

                    # right wall
                    if (tile.get_bb(HB.COLLISION)[POS.LEFT] <=
                            enemy.get_bb(HB.COLLISION)[POS.LEFT] <=
                            tile.get_bb(HB.COLLISION)[POS.RIGHT]
                    ):
                        print("right")
                        enemy.x_direction = game_object.D_RIGHT
                        enemy.facing = enemy.x_direction
                        enemy.set_info()
                        enemy.x = (
                                tile.get_bb(HB.COLLISION)[POS.RIGHT] +
                                enemy.get_bb_range(HB.COLLISION)[POS.LEFT]
                        )
