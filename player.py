from pico2d import *
from game_object import *
from value import *

import gs_framework
import game_object


class KEY(IntEnum):
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
    (SDL_KEYDOWN, SDLK_UP): KEY.UP_DOWN,
    (SDL_KEYUP, SDLK_UP): KEY.UP_UP,
    (SDL_KEYDOWN, SDLK_DOWN): KEY.DOWN_DOWN,
    (SDL_KEYUP, SDLK_DOWN): KEY.DOWN_UP,
    (SDL_KEYDOWN, SDLK_LEFT): KEY.LEFT_DOWN,
    (SDL_KEYUP, SDLK_LEFT): KEY.LEFT_UP,
    (SDL_KEYDOWN, SDLK_RIGHT): KEY.RIGHT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): KEY.RIGHT_UP,
    (SDL_KEYDOWN, SDLK_z): KEY.Z_DOWN,
    (SDL_KEYUP, SDLK_z): KEY.Z_UP,
    (SDL_KEYDOWN, SDLK_x): KEY.X_DOWN,
    (SDL_KEYUP, SDLK_x): KEY.X_UP
}


class IdleState:
    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        pass


class SitState:
    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        pass


class WalkState:
    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        pass


class RunState:
    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        pass


class JumpState:
    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        pass


class FallState:
    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        pass

    def draw(player):
        pass


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
        KEY.UP_DOWN: IdleState, KEY.UP_UP: IdleState,
        KEY.DOWN_DOWN: SitState, KEY.DOWN_UP: SitState,
        KEY.LEFT_DOWN: WalkState, KEY.LEFT_UP: WalkState,
        KEY.RIGHT_DOWN: WalkState, KEY.RIGHT_UP: WalkState,
        KEY.Z_DOWN: RunState, KEY.Z_UP: RunState,
        KEY.X_DOWN: JumpState, KEY.X_UP: IdleState
    },
    SitState: {
        KEY.UP_DOWN: SitState, KEY.UP_UP: SitState,
        KEY.DOWN_UP: IdleState,
        KEY.LEFT_DOWN: WalkState, KEY.LEFT_UP: WalkState,
        KEY.RIGHT_DOWN: WalkState, KEY.RIGHT_UP: WalkState,
        KEY.Z_DOWN: RunState, KEY.Z_UP: RunState,
        KEY.X_DOWN: JumpState, KEY.X_UP: SitState
    },
    WalkState: {
        KEY.UP_DOWN: WalkState, KEY.UP_UP: WalkState,
        KEY.DOWN_DOWN: WalkState, KEY.DOWN_UP: WalkState,
        KEY.LEFT_DOWN: IdleState, KEY.LEFT_UP: IdleState,
        KEY.RIGHT_DOWN: IdleState, KEY.RIGHT_UP: IdleState,
        KEY.Z_DOWN: RunState, KEY.Z_UP: RunState,
        KEY.X_DOWN: JumpState, KEY.X_UP: WalkState
    },
    RunState: {
        KEY.UP_DOWN: RunState, KEY.UP_UP: RunState,
        KEY.DOWN_DOWN: RunState, KEY.DOWN_UP: RunState,
        KEY.LEFT_DOWN: WalkState, KEY.LEFT_UP: WalkState,
        KEY.RIGHT_DOWN: WalkState, KEY.RIGHT_UP: WalkState,
        KEY.Z_DOWN: RunState, KEY.Z_UP: RunState,
        KEY.X_DOWN: JumpState, KEY.X_UP: RunState
    },
    JumpState: {
        KEY.UP_DOWN: JumpState, KEY.UP_UP: JumpState,
        KEY.DOWN_DOWN: JumpState, KEY.DOWN_UP: JumpState,
        KEY.LEFT_DOWN: JumpState, KEY.LEFT_UP: JumpState,
        KEY.RIGHT_DOWN: JumpState, KEY.RIGHT_UP: JumpState,
        KEY.Z_DOWN: JumpState, KEY.Z_UP: JumpState,
        KEY.X_DOWN: JumpState, KEY.X_UP: FallState
    },
    FallState: {
        KEY.UP_DOWN: FallState, KEY.UP_UP: FallState,
        KEY.DOWN_DOWN: FallState, KEY.DOWN_UP: FallState,
        KEY.LEFT_DOWN: FallState, KEY.LEFT_UP: FallState,
        KEY.RIGHT_DOWN: FallState, KEY.RIGHT_UP: FallState,
        KEY.Z_DOWN: FallState, KEY.Z_UP: FallState,
        KEY.X_DOWN: FallState, KEY.X_UP: FallState
    },
    HangState: {
        KEY.UP_DOWN: ClimbState, KEY.UP_UP: ClimbState,
        KEY.DOWN_DOWN: ClimbState, KEY.DOWN_UP: ClimbState,
        KEY.LEFT_DOWN: ClimbState, KEY.LEFT_UP: ClimbState,
        KEY.RIGHT_DOWN: ClimbState, KEY.RIGHT_UP: ClimbState,
        KEY.Z_DOWN: HangState, KEY.Z_UP: HangState,
        KEY.X_DOWN: JumpState, KEY.X_UP: HangState
    },
    ClimbState: {
        KEY.UP_DOWN: HangState, KEY.UP_UP: HangState,
        KEY.DOWN_DOWN: HangState, KEY.DOWN_UP: HangState,
        KEY.LEFT_DOWN: HangState, KEY.LEFT_UP: HangState,
        KEY.RIGHT_DOWN: HangState, KEY.RIGHT_UP: HangState,
        KEY.Z_DOWN: ClimbState, KEY.Z_UP: ClimbState,
        KEY.X_DOWN: JumpState, KEY.X_UP: ClimbState
    }
}


class Player(game_object):
    def __init__(self):
        super(TN.PLAYER, TID.MARIO_SMALL)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

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
#         self.set_clip()
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
#             self.set_clip('jump_down')
#         elif self.is_jump:
#             self.set_clip('jump_up')
#         elif self.is_walk:
#             if self.is_run:
#                 self.set_clip('run')
#             else:
#                 self.set_clip('walk')
#         elif self.is_crawl:
#             self.set_clip('crawl')
#         elif self.is_stay:
#             self.set_clip('stay')
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
#                 self.set_clip()
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
