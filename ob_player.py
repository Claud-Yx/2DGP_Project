from pico2d import *

import game_object
import ob_interactive
import server
from value import *

import gs_framework
import gs_stage_enter

MIN_VELOCITY = get_pps_from_kmph(10.5)

MAX_WALK_VELOCITY = get_pps_from_kmph(23.0)
ACCEL_WALK = get_accel_from_pps(MAX_WALK_VELOCITY, 0.8)

MAX_RUN_VELOCITY = get_pps_from_kmph(55.0)

MAX_JUMP_POWER = get_pps_from_mps(19)
MIN_JUMP_POWER = get_pps_from_mps(8)

JUMP_BOOST_ONE = get_pps_from_mps(3)
JUMP_BOOST_TWO = get_pps_from_mps(6)

STANDARD_INERTIA = ACCEL_WALK * 2.0

CLIMB_VELOCITY = get_pps_from_kmph(23.0)

# Player timer
MAX_TIMER_SHRINK = 0.9
MAX_TIMER_GROW = 1.0
MAX_TIMER_DIE = 3.5
MAX_TIMER_INVINCIBLE = 2.0
MAX_TIMER_STAR_POWER = 8.0


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
    HANGING = auto()
    STAYING = auto()
    WALKING = auto()


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


class Player(game_object.GameObject):
    def __init__(self, tid=TID.MARIO_SMALL, x=0, y=0):

        super().__init__(TN.PLAYER, tid, x, y)

        self.prev_id = tid
        self.is_small = None
        if tid == TID.MARIO_SMALL:
            self.is_small = True
        else:
            self.is_small = False

        self.rx, self.ry = self.ax, self.ay
        self.arx_dist = 0
        self.ary_dist = 0

        if server.stage.x <= gs_framework.canvas_width:
            self.rx += server.stage.x
        if server.stage.y <= gs_framework.canvas_height:
            self.ry += server.stage.y

        # Player inventory
        self.coin = 0
        self.score = 0
        self.life = 5

        # Event and state
        self.event_que = []
        self.cur_state = IdleState
        self.nearby_tiles: Set = set()
        self.nearby_enemies: Set = set()
        self.nearby_items: Set = set()
        self.nearby_interactives: Set = set()

        # Moving value
        self.jump_power = 0
        self.max_jump_power = 0
        self.additional_jump_power = 0

        self.x_accel = 0

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
        self.is_invincible = False
        self.is_star_power = False

        self.on_wire_mesh = None

        self.taken_item = [TN.ITEMS, TID.NONE]

        # Timer
        self.timer_shrink = 0
        self.timer_die = 0
        self.timer_invincible = 0
        self.timer_grow = 0
        self.timer_star_power = 0

        # Setting
        self.set_info()
        self.set_color()
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

        if self.cur_state != SitState:
            if self.on_wire_mesh is not None and event == EVENT.UP_DOWN:
                self.y_direction += DIR.UP
                self.pressed_key_jump = False
                self.add_event(EVENT.HANGING)

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

        self.ax += speed

    def jump(self):
        self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                            ) * -1

        self.jump_power = clamp(
            0, self.jump_power, MAX_JUMP_POWER + self.additional_jump_power
        )

        if self.jump_power == 0:
            self.is_fall = True
            self.is_jump = False

        self.ay += self.jump_power * gs_framework.frame_time

    def fall(self):
        self.jump_power += (GRAVITY_ACCEL_PPS * gs_framework.frame_time * 3
                            ) * -1

        if self.timer_die == 0:
            self.jump_power = clamp(
                MAX_JUMP_POWER * -1, self.jump_power, 0
            )

        self.ay += self.jump_power * gs_framework.frame_time

    def shrink(self) -> bool:
        if self.timer_shrink == 0:
            self.is_invincible = True
            server.stop_time(True, (TN.NONE, TID.NONE))
            if self.cur_state == SitState:
                self.cur_state = IdleState
                self.action = ACTION.IDLE
            self.timer_shrink = MAX_TIMER_SHRINK

        self.timer_shrink -= gs_framework.frame_time

        motion = int(self.timer_shrink * 9) % 3

        self.set_alpha(100)

        if motion == 2:
            if self.type_id == TID.MARIO_SMALL:
                self.ay += 25
                self.ry += 25
            self.set_size()
            self.type_id = self.prev_id
            self.set_clip()
        elif motion == 1:
            if self.wp == 1.0:
                self.ay -= 12.5
                self.ry -= 12.5
            self.set_size(wp=0.75, hp=0.75)
        else:
            if not self.type_id == TID.MARIO_SMALL:
                self.prev_id = self.type_id
                self.ay -= 12.5
                self.ry -= 12.5
            self.type_id = TID.MARIO_SMALL
            self.set_clip()

        self.set_info()
        self.switch_bb_all()

        if self.timer_shrink <= 0.0:
            self.timer_shrink = 0
            return True
        return False

    def grow(self):
        if self.timer_grow == 0:
            server.stop_time(True, (TN.NONE, TID.NONE))
            self.timer_grow = MAX_TIMER_GROW

        self.timer_grow -= gs_framework.frame_time

        motion = int(self.timer_grow * 9) % 3

        if motion == 0:
            if self.type_id == TID.MARIO_SMALL:
                self.ay += 25
                self.ry += 25
            self.set_size()
            self.type_id = self.prev_id
            self.set_clip()
        elif motion == 1:
            if self.wp == 1.0:
                self.ay -= 12.5
                self.ry -= 12.5
            self.set_size(wp=0.75, hp=0.75)
        else:
            if not self.type_id == TID.MARIO_SMALL:
                self.prev_id = self.type_id
                self.ay -= 12.5
                self.ry -= 12.5
            self.type_id = TID.MARIO_SMALL
            self.set_clip()

        if self.timer_grow <= 0.0:
            self.timer_grow = 0
            return True
        return False

    def die(self) -> bool:
        if self.timer_die == 0:
            self.ax, self.ay = self.rx, self.ry
            server.stop_time(True, (TN.NONE, TID.NONE))
            self.is_fall = False
            self.jump_power = MAX_JUMP_POWER
            self.timer_die = MAX_TIMER_DIE
            self.set_info(ACTION.DIE_A)

        self.timer_die -= gs_framework.frame_time

        if self.timer_die < 3.0 and self.ay > -50:
            if not self.is_fall:
                self.jump()
            else:
                self.fall()

            self.rx, self.ry = self.ax, self.ay

        if self.timer_die <= 0.0:
            self.timer_die = 0
            return True
        return False

    def damaged(self):
        if self.is_damaged or self.ry <= -50:
            if self.ry <= -50:
                self.type_id = TID.MARIO_SMALL
            if self.is_small or self.ry <= -50:
                if self.die():
                    gs_framework.change_state(gs_stage_enter)
                    return -1
            else:
                if self.shrink():
                    self.set_size()
                    self.set_alpha()
                    self.switch_bb_all(True)
                    self.is_damaged = False
                    self.is_small = True
                    server.stop_time(False)

    def invincible(self):
        if self.is_invincible and not self.is_damaged:
            if self.timer_invincible == 0:
                self.timer_invincible = MAX_TIMER_INVINCIBLE

            self.timer_invincible -= gs_framework.frame_time

            motion = int(self.timer_invincible * 20) % 2
            if motion == 1:
                self.set_alpha(100)
            else:
                self.set_alpha(200)

            if self.timer_invincible <= 0.0:
                self.timer_invincible = 0.0
                self.is_invincible = False

    def star_power(self):
        if self.is_star_power and not self.is_damaged:
            if self.timer_star_power == 0:
                self.timer_star_power = MAX_TIMER_STAR_POWER

            self.timer_star_power -= gs_framework.frame_time

            motion = int(self.timer_star_power * int(MAX_TIMER_STAR_POWER) * 1.5) % 4
            if motion == 1:
                self.set_color(150, 255, 150)
            elif motion == 2:
                self.set_color(255, 255, 150)
            elif motion == 3:
                self.set_color(150, 150, 255)
            else:
                self.set_color(255, 150, 150)

            if self.timer_star_power <= 0.0:
                self.timer_star_power = 0.0
                self.is_star_power = False
                self.set_color(255, 255, 255)

    def taken_item(self):
        if self.taken_item == (TN.ITEMS, TID.SUPER_MUSHROOM):
            if self.is_small:
                if self.grow():
                    self.set_info()
                    self.is_small = False
                    server.stop_time(False)
                    self.score += 1000
            else:
                self.score += 1000

        elif self.taken_item == (TN.ITEMS, TID.COIN):
            self.coin += 1

        elif self.taken_item == (TN.ITEMS, TID.LIFE_MUSHROOM):
            self.life += 1

        elif self.taken_item == (TN.ITEMS, TID.SUPER_STAR):
            self.is_star_power = True

        if not server.time_stop:
            self.taken_item = (TN.ITEMS, TID.NONE)

    def scroll_and_clamp(self):
        """scroll and clamping"""
        # rx range init
        rx_min, rx_max = gs_framework.canvas_width / 2 - 50, gs_framework.canvas_width / 2 + 50
        ax_max = server.stage.size_width - (
                gs_framework.canvas_width - (gs_framework.canvas_width / 2 + 50)
        )
        # ry range init
        ry_min, ry_max = gs_framework.canvas_height / 2 - 50, gs_framework.canvas_height / 2 + 50
        ay_max = server.stage.size_height - (
                gs_framework.canvas_height - (gs_framework.canvas_height / 2 + 50)
        )

        # range change
        if server.stage.size_width > gs_framework.canvas_width:
            if server.stage.x == 0:
                rx_min = 25
            elif server.stage.x == gs_framework.canvas_width - server.stage.size_width:
                rx_max = gs_framework.canvas_width - 25
        else:
            rx_min, rx_max = 25, gs_framework.canvas_width - 25
        if server.stage.size_height > gs_framework.canvas_height:
            if server.stage.y == 0:
                ry_min = -150
            elif server.stage.y == gs_framework.canvas_height - server.stage.size_height:
                ry_max = gs_framework.canvas_height + 150
        else:
            ry_min, ry_max = -150, gs_framework.canvas_height + 150

        # clamping
        self.ax = clamp(25, self.ax, server.stage.size_width - 25)
        self.ay = clamp(-150, self.ay, server.stage.size_height + 150)

        rx_ran = self.ax
        if self.ax >= ax_max:
            if self.ax >= ax_max and server.stage.size_width > gs_framework.canvas_width:
                rx_ran = self.ax - ax_max + (gs_framework.canvas_width / 2 + 50)
            elif server.stage.size_width <= gs_framework.canvas_width:
                rx_ran = self.ax + server.stage.x

        ry_ran = self.ay
        if self.ay >= ay_max:
            if self.ay >= ay_max and server.stage.size_height > gs_framework.canvas_height:
                ry_ran = self.ay - ay_max + (gs_framework.canvas_height / 2 + 50)
            elif server.stage.size_height <= gs_framework.canvas_height:
                ry_ran = self.ay + server.stage.y

        self.rx = clamp(rx_min, rx_ran, rx_max)
        self.ry = clamp(ry_min, ry_ran, ry_max)
        # delay(0.2)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if self.damaged() == -1:
            return -1

        Player.taken_item(self)

        if server.time_stop:
            return

        self.invincible()
        self.star_power()

        if not self.on_floor and not self.is_jump:
            self.is_fall = True

        # state update
        self.cur_state.do(self)

        self.scroll_and_clamp()

        # new state in
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            # print("cur event: %s" % event)

            # check jump key(x)
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

        debug_print_2 = load_font(os.getenv('PICO2D_DATA_PATH') + '/ConsolaMalgun.TTF', 26)
        debug_print_2.draw(6, gs_framework.canvas_height - 16,
                           # "stage.x/y: (%.2f / %.2f) / player.ap: (%.2f, %.2f) rp: (%.2f, %.2f)" %
                           # (server.stage.x, server.stage.y,
                           #  self.ax, self.ay, self.rx, self.ry),
                           "dry bones action: %s / facing: %s / l,b,h,w : %d / %d / %d / %d" %
                           (server.enemies[0].action, server.enemies[0].facing,
                            server.enemies[0].l, server.enemies[0].b, server.enemies[0].h, server.enemies[0].w),
                           (0, 255, 0))

        if self.show_bb:
            self.draw_bb()

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if ((key_event == EVENT.DOWN_DOWN or key_event == EVENT.DOWN_UP) and
                    self.is_small and self.cur_state != ClimbState):
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
            player.ay += 1
            player.ry += 1
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

        # Running power for jump boosting
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
            player.ay += 1
            player.ry += 1
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

        # Running power for jump boosting
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

        player.ax += speed

    def draw(player: Player):
        player.clip_draw()

class ClimbState:
    def enter(player: Player, event):
        player.velocity = 0
        player.jump_power = 0
        player.is_jump = False
        player.is_fall = False
        player.on_floor = False

        if event == EVENT.RIGHT_DOWN:
            player.x_direction += DIR.RIGHT
        elif event == EVENT.RIGHT_UP:
            player.x_direction += DIR.LEFT
        elif event == EVENT.LEFT_DOWN:
            player.x_direction += DIR.LEFT
        elif event == EVENT.LEFT_UP:
            player.x_direction += DIR.RIGHT
        elif event == EVENT.UP_DOWN:
            player.pressed_key_jump = False
            player.y_direction += DIR.UP
        elif event == EVENT.UP_UP:
            player.y_direction += DIR.DOWN
        elif event == EVENT.DOWN_DOWN:
            player.y_direction += DIR.DOWN
        elif event == EVENT.DOWN_UP:
            player.y_direction += DIR.UP

        if player.x_direction == DIR.NONE and player.y_direction == DIR.NONE:
            player.set_info(ACTION.HANG)
        else:
            player.set_info(ACTION.CLIMB)

    def exit(player: Player, event):
        pass

    def do(player: Player):
        player.update_frame(gs_framework.frame_time)

        if player.x_direction == DIR.NONE and player.y_direction == DIR.NONE:
            player.set_info(ACTION.HANG)
        else:
            player.set_info(ACTION.CLIMB)

        player.velocity = CLIMB_VELOCITY * player.x_direction
        player.jump_power = CLIMB_VELOCITY * player.y_direction
        player.ax += player.velocity * gs_framework.frame_time
        player.ay += player.jump_power * gs_framework.frame_time

        if player.on_wire_mesh is None:
            return

        player.on_wire_mesh: ob_interactive.WireMesh

        x_min = player.on_wire_mesh.get_bb(HB.BODY)[POS.LEFT] + player.get_bb_range(HB.BODY)[POS.LEFT]
        x_max = player.on_wire_mesh.get_bb(HB.BODY)[POS.RIGHT] - player.get_bb_range(HB.BODY)[POS.RIGHT]

        y_min = player.on_wire_mesh.get_bb(HB.BODY)[POS.BOTTOM]
        y_max = player.on_wire_mesh.get_bb(HB.BODY)[POS.TOP] - player.get_bb_range(HB.BODY)[POS.TOP]

        player.ax = clamp(x_min, player.ax, x_max)
        if player.ax <= x_min or player.ax >= x_max:
            player.velocity = 0

        player.ay = clamp(y_min, player.ay, y_max)
        if player.ay >= y_max:
            player.jump_power = 0

        if player.ay <= y_min or player.pressed_key_jump:
            player.y_direction = DIR.NONE

            if player.x_direction == DIR.NONE:
                player.add_event(EVENT.STAYING)
            else:
                player.add_event(EVENT.WALKING)

            if player.pressed_key_jump:
                player.jump_power = MAX_JUMP_POWER
                player.is_fall = False
                player.ay += 1
                player.is_jump = True
                player.set_info(ACTION.JUMP)


    def draw(player: Player):
        player.clip_draw()


next_state_table = {
    IdleState: {
        EVENT.UP_DOWN: IdleState, EVENT.UP_UP: IdleState,
        EVENT.DOWN_DOWN: SitState, EVENT.DOWN_UP: IdleState,
        EVENT.LEFT_DOWN: WalkState, EVENT.LEFT_UP: WalkState,
        EVENT.RIGHT_DOWN: WalkState, EVENT.RIGHT_UP: WalkState,
        EVENT.Z_DOWN: IdleState, EVENT.Z_UP: IdleState,
        EVENT.X_DOWN: IdleState, EVENT.X_UP: IdleState,
        EVENT.HANGING: ClimbState, EVENT.STAYING: IdleState,
        EVENT.WALKING: IdleState
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
        EVENT.X_DOWN: WalkState, EVENT.X_UP: WalkState,
        EVENT.HANGING: ClimbState, EVENT.WALKING: WalkState,
        EVENT.STAYING: WalkState
    },
    ClimbState: {
        EVENT.UP_DOWN: ClimbState, EVENT.UP_UP: ClimbState,
        EVENT.DOWN_DOWN: ClimbState, EVENT.DOWN_UP: ClimbState,
        EVENT.LEFT_DOWN: ClimbState, EVENT.LEFT_UP: ClimbState,
        EVENT.RIGHT_DOWN: ClimbState, EVENT.RIGHT_UP: ClimbState,
        EVENT.Z_DOWN: ClimbState, EVENT.Z_UP: ClimbState,
        EVENT.X_DOWN: ClimbState, EVENT.X_UP: ClimbState,
        EVENT.STAYING: IdleState, EVENT.WALKING: WalkState,
        EVENT.HANGING: ClimbState
    }
}


def test_player():
    from ob_tileset import TileSet
    from collision import \
        collide_player_to_ceiling, collide_player_to_floor, \
        collide_player_to_left_wall, collide_player_to_right_wall

    import test_keyboard

    gs_framework.canvas_width = 1600
    gs_framework.canvas_height = 600

    open_canvas(gs_framework.canvas_width, gs_framework.canvas_height)
    player = Player(TID.MARIO_SMALL, 800, 500)
    tiles = []
    test_keyboard.keyboard_init()

    for x in range(50, 1600, 100):
        tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, x, 50))

    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 50, 350))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 150, 350))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 250, 350))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 250, 450))
    tiles.append(TileSet(TID.CASTLE_BLOCK_100X100, 350, 350))

    def update():
        player.update()

        for floor in tiles:
            if collide_player_to_floor(player, floor):
                break
        for ceiling in tiles:
            if player.is_jump:
                if collide_player_to_ceiling(player, ceiling):
                    break
        for tile in tiles:
            if collide_player_to_right_wall(player, tile):
                break
        for tile in tiles:
            if collide_player_to_left_wall(player, tile):
                break

    Running = True
    show_bb = False

    print("== player info ==")
    print("player.pos = (", player.ax, ", ", player.ay, ")")
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
                    " velocity = " + str(player.velocity) +
                    " action = " + str(player.action) +
                    " is_fall = " + str(player.is_fall))

        update_canvas()

    close_canvas()


if __name__ == "__main__":
    test_player()
