import server
from game_object import *
from value import *

import gs_framework
import game_object

MIN_VELOCITY = get_pps_from_kmph(7.0)

MAX_WALK_VELOCITY = get_pps_from_kmph(19.0)
ACCEL_WALK = get_accel_from_pps(MAX_WALK_VELOCITY, 0.8)

MAX_RUN_VELOCITY = get_pps_from_kmph(51.0)

MAX_JUMP_POWER = get_pps_from_mps(19)
MIN_JUMP_POWER = get_pps_from_mps(8)

JUMP_BOOST_ONE = get_pps_from_mps(2)
JUMP_BOOST_TWO = get_pps_from_mps(4)

STANDARD_INERTIA = ACCEL_WALK * 2.3

# Player timer
MAX_TIMER_SHRINK = 1.0
MAX_TIMER_DIE = 3.0
MAX_TIMER_INVINCIBLE = 3.0


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


class Player(game_object.Object):
    def __init__(self, tid=TID.MARIO_SMALL, x=0, y=0):
        super().__init__(TN.PLAYER, tid, x, y)

        self.prev_id = tid
        self.is_small = None
        if tid == TID.MARIO_SMALL:
            self.is_small = True
        else:
            self.is_small = False

        # Player inventory
        self.coin = 0
        self.score = 0
        self.life = 5

        # Event and state
        self.event_que = []
        self.cur_state = IdleState

        # Moving value
        self.jump_power = 0
        self.max_jump_power = 0
        self.additional_jump_power = 0

        self.x_accel = 0
        self.y_accel = 0

        # Control value
        self.is_stuck_left = False
        self.is_stuck_right = False

        self.is_run = False
        self.is_over_velocity = False

        self.is_sit = False
        self.on_floor = False

        self.is_fall = False
        self.is_jump = False
        self.pressed_key_jump = False

        self.is_damaged = False

        # Setting
        self.set_info()
        self.cur_state.enter(self, None)

        # Timer
        self.timer_shrink = 0

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
            self.forcing = DIR.RIGHT
        elif speed == 0:
            self.forcing = DIR.NONE
        else:
            self.forcing = DIR.LEFT

        self.x += speed

    def jump(self):
        self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                            ) * -1

        self.jump_power = clamp(
            0, self.jump_power, MAX_JUMP_POWER + self.additional_jump_power
        )

        if self.jump_power == 0:
            self.is_fall = True
            self.is_jump = False

        self.y += self.jump_power * gs_framework.frame_time

    def fall(self):
        self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                            ) * -1

        self.jump_power = clamp(
            MAX_JUMP_POWER * -1, self.jump_power, 0
        )

        self.y += self.jump_power * gs_framework.frame_time

    def shrink(self) -> bool:
        if self.timer_shrink == 0:
            server.stop_time(True, (TN.NONE, TID.NONE))
            self.timer_shrink = MAX_TIMER_SHRINK

        self.timer_shrink -= gs_framework.frame_time

        motion = int(self.timer_shrink * 6) % 2

        if motion == 1:
            self.type_id = self.prev_id
        else:
            self.prev_id = self.type_id
            self.type_id = TID.MARIO_SMALL

        self.set_info()

        if self.timer_shrink <= 0.0:
            self.timer_shrink = 0
            return True
        return False

    def die(self) -> bool:
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if self.is_damaged:
            if self.is_small:
                self.die()
            else:
                if self.shrink():
                    self.is_damaged = False
                    self.is_small = True
                    server.stop_time(False)

        if server.time_stop:
            return

        if not self.on_floor and not self.is_jump:
            self.is_fall = True

        self.cur_state.do(self)

        self.x = clamp(25, self.x, gs_framework.canvas_width - 25)
        self.y = clamp(-150, self.y, gs_framework.canvas_width + 150)

        # check jump key(x)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            if event == EVENT.X_DOWN:
                self.pressed_key_jump = True
            elif event == EVENT.X_UP:
                self.pressed_key_jump = False

            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state_table[self.cur_state][event]
            except:
                print('Error State:', self.cur_state.__name__, "Event:", event)
                exit(-1)
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

        debug_print("press_key_jump: " + str(self.pressed_key_jump))

        if self.show_bb:
            self.draw_bb()

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if (key_event == EVENT.DOWN_DOWN or key_event == EVENT.DOWN_UP) and self.is_small:
                return
            self.add_event(key_event)


# ======================================= State ==========================================

class IdleState:
    def enter(player: Player, event):
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
        elif event == EVENT.X_DOWN and not player.is_jump and player.on_floor:
            player.on_floor = False
            player.is_jump = True
            player.jump_power = MAX_JUMP_POWER + player.additional_jump_power
            player.y += 1
            player.set_info(ACTION.JUMP)
            # print("player JP: " + str(player.jump_power))
        elif event == EVENT.X_UP and player.is_jump:
            if player.jump_power >= MIN_JUMP_POWER:
                player.jump_power = MIN_JUMP_POWER

        if player.x_direction == DIR.RIGHT:
            player.facing = DIR.RIGHT
        elif player.x_direction == DIR.LEFT:
            player.facing = DIR.LEFT

    def exit(player: Player, event):
        player.check_state(event)

    def do(player: Player):
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

        slice = (MAX_RUN_VELOCITY - MAX_WALK_VELOCITY) / 5
        if MAX_WALK_VELOCITY + slice * 4 > abs(player.velocity) >= MAX_WALK_VELOCITY + slice / 2:
            player.additional_jump_power = JUMP_BOOST_ONE
        elif abs(player.velocity) >= MAX_WALK_VELOCITY + slice * 4:
            player.additional_jump_power = JUMP_BOOST_TWO
        elif abs(player.velocity) < MAX_WALK_VELOCITY:
            player.additional_jump_power = 0

        player.inertia()

    def draw(player: Player):
        player.clip_draw()


class SitState:
    def enter(player: Player, event):
        if player.on_floor:
            player.set_info(ACTION.SIT)

    def exit(player: Player, event):
        player.check_state(event)

    def do(player: Player):
        player.update_frame(gs_framework.frame_time)

        if player.is_fall:
            player.fall()
            player.set_info(ACTION.FALL)
        elif player.is_jump:
            player.jump()
        elif player.on_floor:
            player.set_info(ACTION.SIT)

        player.inertia()

    def draw(player: Player):
        player.clip_draw()


class WalkState:
    def enter(player: Player, event):
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
        elif event == EVENT.X_DOWN and not player.is_jump and player.on_floor:
            player.on_floor = False
            player.is_jump = True
            player.jump_power = MAX_JUMP_POWER + player.additional_jump_power
            player.y += 1
            player.set_info(ACTION.JUMP)
        elif event == EVENT.X_UP and player.is_jump:
            if player.jump_power >= MIN_JUMP_POWER:
                player.jump_power = MIN_JUMP_POWER

        if player.x_direction == DIR.RIGHT:
            player.facing = DIR.RIGHT
        elif player.x_direction == DIR.LEFT:
            player.facing = DIR.LEFT

        if player.is_run:
            player.max_velocity = MAX_RUN_VELOCITY
        else:
            player.x_accel = ACCEL_WALK
            player.max_velocity = MAX_WALK_VELOCITY

        player.set_info()

        # print("facing: " + str(player.facing) + " direction: " + str(player.x_direction))
        # print(str(player.x_accel), str(player.max_velocity))

    def exit(player: Player, event):
        player.check_state(event)

    def do(player: Player):

        # set player clip set
        if player.is_fall:
            player.fall()
            player.set_info(ACTION.FALL)
        elif player.is_jump:
            player.jump()
        elif player.x_direction != player.forcing and not player.x_direction == DIR.NONE:
            player.set_info(ACTION.BREAK)
        else:
            if player.velocity == 0 and (player.is_stuck_left or player.is_stuck_right):
                player.set_info(ACTION.IDLE)
            elif MAX_WALK_VELOCITY * 1.6 * -1 > player.velocity or MAX_WALK_VELOCITY * 1.6 < player.velocity:
                player.set_info(ACTION.RUN)
            else:
                player.set_info(ACTION.WALK)

        # update frame
        player.update_frame(gs_framework.frame_time)

        # set velocity
        if not player.is_run and player.is_over_velocity:
            player.velocity -= player.x_accel * gs_framework.frame_time * player.x_direction
        else:
            if player.is_jump:
                player.velocity += player.x_accel * gs_framework.frame_time * player.x_direction * 3
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

        # additional jump power

        slice = (MAX_RUN_VELOCITY - MAX_WALK_VELOCITY) / 5
        if MAX_WALK_VELOCITY + slice * 4 > abs(player.velocity) >= MAX_WALK_VELOCITY + slice / 2:
            player.additional_jump_power = JUMP_BOOST_ONE
        elif abs(player.velocity) >= MAX_WALK_VELOCITY + slice * 4:
            player.additional_jump_power = JUMP_BOOST_TWO
        elif abs(player.velocity) < MAX_WALK_VELOCITY:
            player.additional_jump_power = 0

        speed = player.velocity * gs_framework.frame_time

        if speed > 0:
            player.forcing = DIR.RIGHT
        elif speed == 0:
            player.forcing = DIR.NONE
        else:
            player.forcing = DIR.LEFT


        player.x += speed

    def draw(player: Player):
        player.clip_draw()


class HangState:
    def enter(player: Player, event):
        pass

    def exit(player: Player, event):
        pass

    def do(player: Player):
        pass

    def draw(player: Player):
        pass


class ClimbState:
    def enter(player: Player, event):
        pass

    def exit(player: Player, event):
        pass

    def do(player: Player):
        pass

    def draw(player: Player):
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
        EVENT.DOWN_DOWN: SitState, EVENT.DOWN_UP: IdleState,
        EVENT.LEFT_DOWN: WalkState, EVENT.LEFT_UP: WalkState,
        EVENT.RIGHT_DOWN: WalkState, EVENT.RIGHT_UP: WalkState,
        EVENT.Z_DOWN: SitState, EVENT.Z_UP: SitState,
        EVENT.X_DOWN: IdleState, EVENT.X_UP: IdleState
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


def test_player():
    from ob_tileset import TileSet
    import test_keyboard

    gs_framework.canvas_width = 1600
    gs_framework.canvas_height = 600

    open_canvas(gs_framework.canvas_width, gs_framework.canvas_height)
    player = Player(TID.MARIO_SUPER, 800, 500)
    tiles = []
    test_keyboard.keyboard_init()

    for x in range(50, 1600, 100):
        tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, x, 50))

    # tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 750, 150))
    # tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 850, 150))
    # tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 850, 250))
    # tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 250, 350))
    # tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 350, 350))

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
            if (player.get_bb_on(HB.STAND) and tile.get_bb_on(HB.BODY) and
                    collide(player.get_bb(HB.STAND),
                            tile.get_bb(HB.BODY)
                            )
            ):
                player.jump_power = 0
                player.on_floor = True
                player.is_fall = False
                player.is_jump = False

                if (player.get_bb(HB.STAND)[POS.BOTTOM] < tile.get_bb(HB.BODY)[POS.TOP] and
                        player.action != ACTION.JUMP):
                    player.y = (
                            player.bounding_box[HB.STAND].range[POS.BOTTOM] +
                            tile.get_bb(HB.BODY)[POS.TOP]
                    )

                break
            elif (player.get_bb_on(HB.STAND) and tile.get_bb_on(HB.BODY) and
                  not collide(
                      player.get_bb(HB.STAND),
                      tile.get_bb(HB.BODY)
                  )
            ):
                player.on_floor = False

        for tile in tiles:
            if (player.get_bb_on(HB.BODY) and
                    tile.get_bb_on(HB.BODY) and
                    collide(player.get_bb(HB.BODY),
                            tile.get_bb(HB.BODY)
                            ) and
                    player.get_bb(HB.BODY)[POS.BOTTOM] < tile.get_bb(HB.BODY)[POS.TOP]
            ):

                # ceiling
                if (tile.get_bb(HB.BODY)[POS.BOTTOM] <=
                        player.get_bb(HB.BODY)[POS.TOP] <=
                        tile.get_bb(HB.BODY)[POS.TOP] and
                        tile.get_bb(HB.BODY)[POS.LEFT] <=
                        player.get_bb(HB.BODY)[POS.RIGHT] <=
                        tile.get_bb(HB.BODY)[POS.RIGHT] and
                        tile.get_bb(HB.BODY)[POS.LEFT] <=
                        player.get_bb(HB.BODY)[POS.LEFT] <=
                        tile.get_bb(HB.BODY)[POS.RIGHT]
                ):
                    player.jump_power = 0
                    player.y = (
                            tile.get_bb(HB.BODY)[POS.BOTTOM] -
                            player.get_bb_range(HB.BODY)[POS.TOP]
                    )

                else:
                    # left wall
                    if (tile.get_bb(HB.BODY)[POS.RIGHT] >=
                            player.get_bb(HB.BODY)[POS.RIGHT] >=
                            tile.get_bb(HB.BODY)[POS.LEFT]
                    ):
                        if player.facing == DIR.RIGHT:
                            player.velocity = 0
                        player.x = (
                                tile.get_bb(HB.BODY)[POS.LEFT] -
                                player.get_bb_range(HB.BODY)[POS.RIGHT]
                        )

                    # right wall
                    if (tile.get_bb(HB.BODY)[POS.LEFT] <=
                            player.get_bb(HB.BODY)[POS.LEFT] <=
                            tile.get_bb(HB.BODY)[POS.RIGHT]
                    ):
                        if player.facing == DIR.LEFT:
                            player.velocity = 0
                        player.x = (
                                tile.get_bb(HB.BODY)[POS.RIGHT] +
                                player.get_bb_range(HB.BODY)[POS.LEFT]
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
                test_keyboard.keyboard_handle(events)

        update()
        player.update()

        keyboard_size = 0.75
        test_keyboard.update_test_keyboard(
            pico2d.get_canvas_width() - (64 * 4 + 50) * keyboard_size,
            pico2d.get_canvas_height() - 50 * keyboard_size,
            keyboard_size, keyboard_size
        )

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
