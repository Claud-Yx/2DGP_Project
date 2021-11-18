from game_object import *
from value import *

import gs_framework
import game_object

MIN_VELOCITY = get_pps_from_kmph(7.0)

MAX_WALK_VELOCITY = get_pps_from_kmph(19.0)
ACCEL_WALK = get_accel_from_pps(MAX_WALK_VELOCITY, 0.8)

MAX_RUN_VELOCITY = get_pps_from_kmph(51.0)

MAX_JUMP_POWER = get_pps_from_mps(20)

STANDARD_INERTIA = ACCEL_WALK * 2.3


class EVENT(IntEnum):
    UP_DOWN = 0
    UP_UP = auto()
    DOWN_DOWN = auto()
    DOWN_UP = auto()
    LEFT_DOWN = auto()
    LEFT_UP = auto()
    RIGHT_DOWN = auto()
    RIGHT_UP = auto()
    Z_DOWN = auto()
    Z_UP = auto()
    X_DOWN = auto()
    X_UP = auto()


key_event_table = {
    (SDL_KEYDOWN, SDLK_UP): EVENT.UP_DOWN,
    (SDL_KEYUP, SDLK_UP): EVENT.UP_UP,
    (SDL_KEYDOWN, SDLK_DOWN): EVENT.DOWN_DOWN,
    (SDL_KEYUP, SDLK_DOWN): EVENT.DOWN_UP,
    (SDL_KEYDOWN, SDLK_LEFT): EVENT.LEFT_DOWN,
    (SDL_KEYUP, SDLK_LEFT): EVENT.LEFT_UP,
    (SDL_KEYDOWN, SDLK_RIGHT): EVENT.RIGHT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): EVENT.RIGHT_UP,
    (SDL_KEYDOWN, SDLK_z): EVENT.Z_DOWN,
    (SDL_KEYUP, SDLK_z): EVENT.Z_UP,
    (SDL_KEYDOWN, SDLK_x): EVENT.X_DOWN,
    (SDL_KEYUP, SDLK_x): EVENT.X_UP
}


class IdleState:
    def enter(player, event):
        if player.is_sit:
            player.add_event(EVENT.DOWN_DOWN)

        if event == EVENT.RIGHT_DOWN:
            player.x_direction += 1
        elif event == EVENT.RIGHT_UP:
            player.x_direction -= 1
        elif event == EVENT.LEFT_DOWN:
            player.x_direction -= 1
        elif event == EVENT.LEFT_UP:
            player.x_direction += 1
        elif event == EVENT.X_DOWN and player.on_floor:
            player.on_floor = False
            player.is_jump = True
            player.jump_power = MAX_JUMP_POWER
            player.set_info(ACTION.JUMP)

        if player.x_direction == D_RIGHT:
            player.facing = D_RIGHT
        elif player.x_direction == D_LEFT:
            player.facing = D_LEFT

    def exit(player, event):
        player.check_state(event)

    def do(player):
        player.update_frame(gs_framework.frame_time)

        if player.is_fall:
            player.fall()
            player.set_info(ACTION.FALL)
        elif player.is_jump:
            player.jump()
        elif player.velocity == 0:
            player.set_info(ACTION.IDLE)
        else:
            player.set_info(ACTION.WALK)

        player.inertia()

    def draw(player):
        player.clip_draw()


class SitState:
    def enter(player, event):
        player.set_info(ACTION.SIT)

        if event == EVENT.X_DOWN and player.on_floor:
            player.on_floor = False
            player.is_jump = True
            player.jump_power = MAX_JUMP_POWER
            player.bounding_box[HB.STAND].is_on = False

    def exit(player, event):
        player.check_state(event)

    def do(player):
        player.update_frame(gs_framework.frame_time)

        if player.is_fall:
            player.fall()
            player.set_info(ACTION.FALL)
        elif player.is_jump:
            player.jump()
        else:
            player.set_info(ACTION.SIT)

        player.inertia()

    def draw(player):
        player.clip_draw()


class WalkState:
    def enter(player, event):
        if event == EVENT.RIGHT_DOWN:
            player.x_direction += 1
            if player.is_fall:
                player.velocity += MIN_VELOCITY * player.x_direction * 3
            else:
                player.velocity += MIN_VELOCITY * player.x_direction
        elif event == EVENT.RIGHT_UP:
            player.x_direction -= 1
        elif event == EVENT.LEFT_DOWN:
            player.x_direction -= 1
            if player.is_fall:
                player.velocity += MIN_VELOCITY * player.x_direction * 3
            else:
                player.velocity += MIN_VELOCITY * player.x_direction
        elif event == EVENT.LEFT_UP:
            player.x_direction += 1

        # jump key down
        elif event == EVENT.X_DOWN and player.on_floor:
            player.on_floor = False
            player.is_jump = True
            player.jump_power = MAX_JUMP_POWER
            player.set_info(ACTION.JUMP)
            print("player jump power: " + str(player.jump_power) + " is_jump: " + str(player.is_jump))

        if player.x_direction == D_RIGHT:
            player.facing = D_RIGHT
        elif player.x_direction == D_LEFT:
            player.facing = D_LEFT

        if player.is_run:
            player.max_velocity = MAX_RUN_VELOCITY
        else:
            player.x_accel = ACCEL_WALK
            player.max_velocity = MAX_WALK_VELOCITY

        player.set_info()

        # print("facing: " + str(player.facing) + " direction: " + str(player.x_direction))
        # print(str(player.x_accel), str(player.max_velocity))

    def exit(player, event):
        player.check_state(event)

    def do(player):

        # set player clip set
        if player.is_fall:
            player.fall()
            player.set_info(ACTION.FALL)
        elif player.is_jump:
            player.jump()
        elif player.x_direction != player.forcing:
            player.set_info(ACTION.BREAK)
        else:
            if MAX_WALK_VELOCITY * 1.6 * -1 > player.velocity or MAX_WALK_VELOCITY * 1.6 < player.velocity:
                player.set_info(ACTION.RUN)
            else:
                player.set_info(ACTION.WALK)

        # update frame
        player.update_frame(gs_framework.frame_time)

        # set velocity
        if not player.is_run and player.is_over_velocity:
            player.velocity -= player.x_accel * gs_framework.frame_time * player.x_direction
        else:
            player.velocity += player.x_accel * gs_framework.frame_time * player.x_direction

        # if player break:
        if player.forcing != player.x_direction:
            player.velocity += (player.x_accel * gs_framework.frame_time +
                                STANDARD_INERTIA * gs_framework.frame_time) * player.x_direction * 1.7

        # clamp player
        if player.is_run or not player.is_over_velocity:
            player.velocity = clamp(player.max_velocity * -1, player.velocity, player.max_velocity)
        else:
            player.velocity = clamp(MAX_RUN_VELOCITY * -1, player.velocity, MAX_RUN_VELOCITY)

        # check over walk velocity
        if player.velocity < MAX_WALK_VELOCITY * -1 or player.velocity > MAX_WALK_VELOCITY:
            player.is_over_velocity = True
        else:
            player.is_over_velocity = False

        speed = player.velocity * gs_framework.frame_time

        if speed > 0:
            player.forcing = D_RIGHT
        elif speed == 0:
            player.forcing = D_NONE
        else:
            player.forcing = D_LEFT

        player.x += speed

    def draw(player):
        player.clip_draw()


class HangState:
    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        pass


class ClimbState:
    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        pass


next_state_table = {
    IdleState: {
        EVENT.UP_DOWN: IdleState, EVENT.UP_UP: IdleState,
        EVENT.DOWN_DOWN: SitState, EVENT.DOWN_UP: IdleState,
        EVENT.LEFT_DOWN: WalkState, EVENT.LEFT_UP: WalkState,
        EVENT.RIGHT_DOWN: WalkState, EVENT.RIGHT_UP: WalkState,
        EVENT.Z_DOWN: IdleState, EVENT.Z_UP: IdleState,
        EVENT.X_DOWN: IdleState, EVENT.X_UP: IdleState
    },
    SitState: {
        EVENT.UP_DOWN: SitState, EVENT.UP_UP: SitState,
        EVENT.DOWN_UP: IdleState,
        EVENT.LEFT_DOWN: WalkState, EVENT.LEFT_UP: WalkState,
        EVENT.RIGHT_DOWN: WalkState, EVENT.RIGHT_UP: WalkState,
        EVENT.Z_DOWN: SitState, EVENT.Z_UP: SitState,
        EVENT.X_DOWN: SitState, EVENT.X_UP: SitState
    },
    WalkState: {
        EVENT.UP_DOWN: WalkState, EVENT.UP_UP: WalkState,
        EVENT.DOWN_DOWN: WalkState, EVENT.DOWN_UP: WalkState,
        EVENT.LEFT_DOWN: IdleState, EVENT.LEFT_UP: IdleState,
        EVENT.RIGHT_DOWN: IdleState, EVENT.RIGHT_UP: IdleState,
        EVENT.Z_DOWN: WalkState, EVENT.Z_UP: WalkState,
        EVENT.X_DOWN: WalkState, EVENT.X_UP: WalkState
    },
    # JumpState: {
    #     KEY.UP_DOWN: JumpState, KEY.UP_UP: JumpState,
    #     KEY.DOWN_DOWN: JumpState, KEY.DOWN_UP: JumpState,
    #     KEY.LEFT_DOWN: JumpState, KEY.LEFT_UP: JumpState,
    #     KEY.RIGHT_DOWN: JumpState, KEY.RIGHT_UP: JumpState,
    #     KEY.Z_DOWN: JumpState, KEY.Z_UP: JumpState,
    #     KEY.X_DOWN: JumpState, KEY.X_UP: FallState
    # },
    HangState: {
        EVENT.UP_DOWN: ClimbState, EVENT.UP_UP: ClimbState,
        EVENT.DOWN_DOWN: ClimbState, EVENT.DOWN_UP: ClimbState,
        EVENT.LEFT_DOWN: ClimbState, EVENT.LEFT_UP: ClimbState,
        EVENT.RIGHT_DOWN: ClimbState, EVENT.RIGHT_UP: ClimbState,
        EVENT.Z_DOWN: HangState, EVENT.Z_UP: HangState,
        EVENT.X_DOWN: HangState, EVENT.X_UP: HangState
    },
    ClimbState: {
        EVENT.UP_DOWN: HangState, EVENT.UP_UP: HangState,
        EVENT.DOWN_DOWN: HangState, EVENT.DOWN_UP: HangState,
        EVENT.LEFT_DOWN: HangState, EVENT.LEFT_UP: HangState,
        EVENT.RIGHT_DOWN: HangState, EVENT.RIGHT_UP: HangState,
        EVENT.Z_DOWN: ClimbState, EVENT.Z_UP: ClimbState,
        EVENT.X_DOWN: ClimbState, EVENT.X_UP: ClimbState
    }
}


class Player(game_object.Object):
    def __init__(self, tid=TID.MARIO_SMALL, x=0, y=0):
        super().__init__(TN.PLAYER, tid, x, y)

        # Event and state
        self.event_que = []
        self.cur_state = IdleState

        # Moving value
        self.jump_power = 0
        self.max_jump_power = 0
        self.x_accel = 0
        self.y_accel = 0

        # Control value
        self.is_run = False
        self.is_over_velocity = False

        self.is_sit = False
        self.on_floor = False

        self.is_fall = False
        self.is_jump = False

        self.set_info()
        self.cur_state.enter(self, None)

    def check_state(self, event):
        if event == EVENT.Z_DOWN:
            self.is_run = True
        elif event == EVENT.Z_UP:
            self.is_run = False
        elif event == EVENT.DOWN_DOWN:
            self.is_sit = True
        elif event == EVENT.DOWN_UP:
            self.is_sit = False

    def inertia(self):
        self.velocity -= STANDARD_INERTIA * gs_framework.frame_time * self.forcing

        if -1 < self.velocity < 1:
            self.velocity = 0

        speed = self.velocity * gs_framework.frame_time

        if speed > 0:
            self.forcing = D_RIGHT
        elif speed == 0:
            self.forcing = D_NONE
        else:
            self.forcing = D_LEFT

        self.x += speed

    def jump(self):
        self.jump_power += (
                                   GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                           ) * -1

        self.jump_power = clamp(
            0, self.jump_power, MAX_JUMP_POWER
        )

        if self.jump_power == 0:
            self.is_fall = True
            self.is_jump = False

        self.y += self.jump_power * gs_framework.frame_time

    def fall(self):
        self.jump_power += (
                                   GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                           ) * -1

        self.jump_power = clamp(
            MAX_JUMP_POWER * -1, self.jump_power, 0
        )

        self.y += self.jump_power * gs_framework.frame_time

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if not self.on_floor and not self.is_jump:
            self.is_fall = True

        self.cur_state.do(self)

        self.x = clamp(25, self.x, gs_framework.canvas_width - 25)
        self.y = clamp(-150, self.y, gs_framework.canvas_width + 150)

        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state_table[self.cur_state][event]
            except:
                print('Error State:', self.cur_state.__name__, "Event:", event)
                exit(-1)
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

        if self.show_bb:
            self.draw_bb()

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


def test_player():
    from tileset import TileSet

    gs_framework.canvas_width = 1600
    gs_framework.canvas_height = 600

    open_canvas(gs_framework.canvas_width, gs_framework.canvas_height)
    player = Player(TID.MARIO_SUPER, 800, 500)
    tiles = []

    for x in range(50, 1600, 100):
        tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, x, 50))

    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 750, 150))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 850, 150))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 850, 250))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 250, 350))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 350, 350))

    def collide(a: (0, 0, 0, 0), b: (0, 0, 0, 0)):
        left_a, bottom_a, right_a, top_a = a
        left_b, bottom_b, right_b, top_b = b

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

    def update():
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
                        if player.facing == game_object.D_RIGHT:
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
                        if player.facing == game_object.D_LEFT:
                            player.velocity = 0
                        player.x = (
                                tile.get_bb(HB.COLLISION)[POS.RIGHT] +
                                player.get_bb_range(HB.COLLISION)[POS.LEFT]
                        )


    Running = True
    show_bb = False

    print("== player info ==")
    print("player.pos = (", player.x, ", ", player.y, ")")
    print("player.cur_state = " + player.cur_state.__name__)

    current_time = get_time()

    while Running:
        clear_canvas()
        gs_framework.frame_time = get_time() - current_time
        current_time += gs_framework.frame_time
        events = get_events()

        for event in events:
            if event.type == SDL_QUIT:
                Running = False
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Running = False
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F2):
                print("in debugging")
                if not show_bb:
                    show_bb = True
                    player.show_bb = True

                    for tile in tiles:
                        tile.show_bb = True
                else:
                    show_bb = False
                    player.show_bb = False

                    for tile in tiles:
                        tile.show_bb = False

            else:
                player.handle_event(event)

        update()
        player.update()

        for tile in tiles:
            tile.draw()

        player.draw()

        debug_print(" facing = " + str(player.facing) +
                    " x_dir = " + str(player.x_direction) +
                    " velocity = " + str(player.velocity))

        update_canvas()

    close_canvas()


if __name__ == "__main__":
    test_player()

# class Player(Character_Object):
#     def __init__(self, x, y):
#         super(Player, self).__init__()
#         self.x, self.y = x, y
#         self.wx, self.wy = x, y
#
#         # 임시 점프
#         self.jump_power_max = 20
#         self.jump_power = self.jump_power_max
#
#         # 임시 중력
#         self.gravity = 0
#
#         self.action = "stay"
#         self.direction = D_RIGHT
#         self.moving_dir = 0
#         self.speed = 6
#         self.acceleration = 3
#         self.state = s
#         self.update_state()
#         self.set_info()
#
#         self.is_stay = True
#         self.is_walk = False
#         self.is_run = False
#         self.is_crawl = False
#         self.is_jump = False
#         self.is_fall = False
#
#         self.is_float = False
#         self.is_stuck_r = False
#         self.is_stuck_l = False
#
#         # Hit box debugging
#         self.is_show_hit_box = False
#         self.is_show_object_box = False
#
#     def switch_stay(self, bl=True):
#         self.is_stay = bl
#         if self.is_stay:
#             self.is_walk = False
#         else:
#             pass
#
#     def switch_walk(self, bl=True):
#         self.is_walk = bl
#         if self.is_walk:
#             self.is_stay = False
#         else:
#             pass
#
#     def switch_run(self, bl=True):
#         self.is_run = bl
#
#     def switch_crawl(self, bl=True):
#         self.is_crawl = bl
#
#     def switch_jump(self, bl=True):
#         self.is_jump = bl
#         if self.is_jump:
#             self.is_fall = False
#             self.switch_float()
#
#     def switch_fall(self, bl=True):
#         self.is_fall = bl
#         if self.is_fall:
#             self.is_jump = False
#             self.is_crawl = False
#             self.switch_float()
#
#     def switch_float(self, bl=True):
#         self.is_float = bl
#         if self.is_float:
#             self.is_crawl = False
#
#     def switch_stuck_r(self, bl=True):
#         self.is_stuck_r = bl
#
#     def switch_stuck_l(self, bl=True):
#         self.is_stuck_l = bl
#
#     def full_jump(self):
#         self.jump_power = self.jump_power_max
#
#     def reset_boxes_pos(self):
#         self.hit_box.set_pos(self.x, self.y)
#         self.stand_box.set_pos(self.x, self.y)
#         self.attack_box.set_pos(self.x, self.y)
#         self.break_box.set_pos(self.x, self.y)
#
#     def update_state(self):
#         if self.state == PS_SMALL:
#             self.image_id = CO_MARIO_SMALL
#         elif self.state == PS_SUPER:
#             self.image_id = CO_MARIO_SUPER
#
#     def update_animation(self):
#
#         if self.is_fall:
#             self.set_info('jump_down')
#         elif self.is_jump:
#             self.set_info('jump_up')
#         elif self.is_walk:
#             if self.is_run:
#                 self.set_info('run')
#             else:
#                 self.set_info('walk')
#         elif self.is_crawl:
#             self.set_info('crawl')
#         elif self.is_stay:
#             self.set_info('stay')
#
#     def update_move(self):
#         if self.is_fall and not self.is_jump:
#             self.y -= self.gravity
#             self.gravity += 1
#             if self.gravity >= self.jump_power_max:
#                 self.gravity = self.jump_power_max
#         elif self.is_jump:
#             self.y += self.jump_power
#             self.jump_power -= 1
#             if self.jump_power < 0:
#                 self.jump_power = 0
#                 self.switch_fall()
#
#         if self.moving_dir == D_NONE:
#             if not self.is_stay:
#                 self.switch_stay()
#         else:
#             if self.is_stay:
#                 self.switch_walk(True)
#             if self.direction != self.moving_dir:
#                 self.direction = self.moving_dir
#                 self.set_info()
#
#             if self.is_walk and (not self.is_stuck_r and not self.is_stuck_l):
#                 if self.is_run:
#                     self.x += (self.speed + self.acceleration) * self.moving_dir
#                 else:
#                     self.x += self.speed * self.moving_dir
#
#         if self.x < 0:
#             self.x = 0
#         elif self.x >= 800:
#             self.x = 800 - 1
#
#         self.hit_box.set_pos(self.x, self.y)
#         self.stand_box.set_pos(self.x, self.y)
#         self.attack_box.set_pos(self.x, self.y)
#         self.break_box.set_pos(self.x, self.y)
#
#         # print("update move: ", self.direction, self.moving_dir, self.action)
#
#     def update_hit_box(self):
#
#         while 0 < len(self.stand_box.other_type_name) and self.stand_box.is_on:
#             o_name = self.stand_box.other_type_name.pop()
#             o_type = self.stand_box.other_type_id.pop()
#             o_pos = self.stand_box.other_center_pos.pop()
#             o_range = self.stand_box.other_range.pop()
#             o_range_pos = self.stand_box.other_range_pos.pop()
#             o_edge_pos = self.stand_box.other_edge_pos.pop()
#             stand = self.stand_box.hit.pop()
#
#             if (
#                     stand[POS.BOTTOM] and
#                     not self.is_jump and
#                     self.py >= o_range_pos[POS.TOP] + self.stand_box.range[POS.BOTTOM]
#             ):
#
#                 if (
#                         o_type == TYPE.PLATFORM_T or
#                         o_type == TYPE.PLATFORM_NT
#                 ):
#                     self.y = o_range_pos[POS.TOP] + self.stand_box.range[POS.BOTTOM]
#                     self.full_jump()
#                     self.gravity = 0
#                     self.switch_fall(False)
#                     self.switch_float(False)
#                     self.reset_boxes_pos()
#
#         while 0 < len(self.hit_box.other_type_name) and self.hit_box.is_on:
#             o_name = self.hit_box.other_type_name.pop()
#             o_type = self.hit_box.other_type_id.pop()
#             o_pos = self.hit_box.other_center_pos.pop()
#             o_range = self.hit_box.other_range.pop()
#             o_range_pos = self.hit_box.other_range_pos.pop()
#             o_edge_pos = self.hit_box.other_edge_pos.pop()
#             hit = self.hit_box.hit.pop()
#
#             if (
#                     hit[POS.TOP] and
#                     not hit[POS.BOTTOM] and
#                     self.py <= o_range_pos[POS.BOTTOM] - self.hit_box.range[POS.TOP]
#             ):
#                 self.y = o_range_pos[POS.BOTTOM] - self.hit_box.range[POS.TOP] - 1
#                 self.switch_fall()
#                 self.gravity = 0
#
#             elif (
#                     hit[POS.RIGHT] and
#                     not hit[POS.LEFT] and
#                     self.x < o_range_pos[POS.LEFT] and
#                     self.hit_box.range_pos[POS.BOTTOM] < o_range_pos[POS.TOP]
#             ):
#                 self.x = o_range_pos[POS.LEFT] - self.hit_box.range[POS.RIGHT]
#                 self.reset_boxes_pos()
#                 self.switch_stuck_r()
#
#             elif (
#                     hit[POS.LEFT] and
#                     not hit[POS.RIGHT] and
#                     self.x > o_range_pos[POS.RIGHT] and
#                     self.hit_box.range_pos[POS.BOTTOM] < o_range_pos[POS.TOP]
#             ):
#                 self.x = o_range_pos[POS.RIGHT] + self.hit_box.range[POS.LEFT]
#                 self.reset_boxes_pos()
#                 self.switch_stuck_l()
#
#         if self.hit_box.is_on:
#             if not self.is_jump and not self.hit_box.is_hit[POS.BOTTOM]:
#                 self.switch_fall()
#
#             if (
#                     (not self.hit_box.is_hit[POS.RIGHT]
#                      or self.direction == D_LEFT)
#             ):
#                 self.switch_stuck_r(False)
#
#             if (
#                     (not self.hit_box.is_hit[POS.LEFT]
#                      or self.direction == D_RIGHT)
#             ):
#                 self.switch_stuck_l(False)
#
#         self.hit_box.is_hit = [False for b in range(len(self.hit_box.is_hit))]
#
#         self.hit_box.set_pos(self.x, self.y)
#         self.stand_box.set_pos(self.x, self.y)
#         self.attack_box.set_pos(self.x, self.y)
#         self.break_box.set_pos(self.x, self.y)
#
#     def update(self):
#         self.px, self.py = self.x, self.y
#         self.update_state()
#         # self.update_hit_box()
#         self.update_move()
#         self.update_animation()
#
#     def handle_event(self, events):
#         # events = get_events()
#
#         for event in events:
#             if event.type_id == SDL_QUIT:
#                 gs_framework.quit()
#
#             elif event.type_id == SDL_KEYDOWN:
#                 if event.key == SDLK_ESCAPE:
#                     return False
#
#                 elif event.key == SDLK_F3:
#                     if self.is_show_hit_box:
#                         self.is_show_hit_box = False
#                     else:
#                         self.is_show_hit_box = True
#
#                 elif event.key == SDLK_F2:
#                     if self.is_show_object_box:
#                         self.is_show_object_box = False
#                     else:
#                         self.is_show_object_box = True
#
#                 elif event.key == SDLK_RIGHT:
#                     self.direction = D_RIGHT
#                     self.moving_dir += D_RIGHT
#                     self.switch_walk()
#                 elif event.key == SDLK_LEFT:
#                     self.direction = D_LEFT
#                     self.moving_dir += D_LEFT
#                     self.switch_walk()
#                 elif event.key == SDLK_UP:
#                     pass
#                 elif event.key == SDLK_DOWN:
#                     if self.state != PS_SMALL:
#                         self.switch_crawl()
#
#                 elif event.key == SDLK_z:
#                     self.switch_run()
#                 elif event.key == SDLK_x:
#                     if not self.is_fall:
#                         self.switch_jump()
#
#             elif event.type_id == SDL_KEYUP:
#
#                 if event.key == SDLK_RIGHT:
#                     self.moving_dir += D_LEFT
#                 elif event.key == SDLK_LEFT:
#                     self.moving_dir += D_RIGHT
#                 elif event.key == SDLK_UP:
#                     pass
#                 elif event.key == SDLK_DOWN:
#                     if self.state != PS_SMALL:
#                         self.switch_crawl(False)
#
#                 elif event.key == SDLK_z:
#                     self.switch_run(False)
#                 elif event.key == SDLK_x:
#                     if self.is_jump and not self.is_fall:
#                         self.switch_fall()
#                         self.jump_power = 0
#
#         return True
