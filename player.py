from pico2d import *

import gs_framework
from character_object import *

PS_SMALL = 0
PS_SUPER = 1


class Player(Character_Object):
    def __init__(self, x, y, s=PS_SMALL):
        super(Player, self).__init__()
        self.x, self.y = x, y
        self.wx, self.wy = x, y

        # 임시 점프
        self.jump_power_max = 20
        self.jump_power = self.jump_power_max

        # 임시 중력
        self.gravity = 0

        self.action = "stay"
        self.direction = D_RIGHT
        self.moving_dir = 0
        self.speed = 6
        self.acceleration = 3
        self.state = s
        self.update_state()
        self.set_clip()

        self.is_stay = True
        self.is_walk = False
        self.is_run = False
        self.is_crawl = False
        self.is_jump = False
        self.is_fall = False

        self.is_float = False
        self.is_stuck_r = False
        self.is_stuck_l = False

        # Hit box debugging
        self.is_show_hit_box = False
        self.is_show_object_box = False

    def switch_stay(self, bl=True):
        self.is_stay = bl
        if self.is_stay:
            self.is_walk = False
        else:
            pass

    def switch_walk(self, bl=True):
        self.is_walk = bl
        if self.is_walk:
            self.is_stay = False
        else:
            pass

    def switch_run(self, bl=True):
        self.is_run = bl

    def switch_crawl(self, bl=True):
        self.is_crawl = bl

    def switch_jump(self, bl=True):
        self.is_jump = bl
        if self.is_jump:
            self.is_fall = False
            self.switch_float()

    def switch_fall(self, bl=True):
        self.is_fall = bl
        if self.is_fall:
            self.is_jump = False
            self.is_crawl = False
            self.switch_float()

    def switch_float(self, bl=True):
        self.is_float = bl
        if self.is_float:
            self.is_crawl = False

    def switch_stuck_r(self, bl=True):
        self.is_stuck_r = bl

    def switch_stuck_l(self, bl=True):
        self.is_stuck_l = bl

    def full_jump(self):
        self.jump_power = self.jump_power_max

    def reset_boxes_pos(self):
        self.hit_box.set_pos(self.x, self.y)
        self.stand_box.set_pos(self.x, self.y)
        self.attack_box.set_pos(self.x, self.y)
        self.break_box.set_pos(self.x, self.y)

    def update_state(self):
        if self.state == PS_SMALL:
            self.image_id = CO_MARIO_SMALL
        elif self.state == PS_SUPER:
            self.image_id = CO_MARIO_SUPER

    def update_animation(self):

        if self.is_fall:
            self.set_clip('jump_down')
        elif self.is_jump:
            self.set_clip('jump_up')
        elif self.is_walk:
            if self.is_run:
                self.set_clip('run')
            else:
                self.set_clip('walk')
        elif self.is_crawl:
            self.set_clip('crawl')
        elif self.is_stay:
            self.set_clip('stay')

    def update_move(self):
        if self.is_fall and not self.is_jump:
            self.y -= self.gravity
            self.gravity += 1
            if self.gravity >= self.jump_power_max:
                self.gravity = self.jump_power_max
        elif self.is_jump:
            self.y += self.jump_power
            self.jump_power -= 1
            if self.jump_power < 0:
                self.jump_power = 0
                self.switch_fall()

        if self.moving_dir == D_NONE:
            if not self.is_stay:
                self.switch_stay()
        else:
            if self.is_stay:
                self.switch_walk(True)
            if self.direction != self.moving_dir:
                self.direction = self.moving_dir
                self.set_clip()

            if self.is_walk and (not self.is_stuck_r and not self.is_stuck_l):
                if self.is_run:
                    self.x += (self.speed + self.acceleration) * self.moving_dir
                else:
                    self.x += self.speed * self.moving_dir

        if self.x < 0:
            self.x = 0
        elif self.x >= 800:
            self.x = 800 - 1

        self.hit_box.set_pos(self.x, self.y)
        self.stand_box.set_pos(self.x, self.y)
        self.attack_box.set_pos(self.x, self.y)
        self.break_box.set_pos(self.x, self.y)

        # print("update move: ", self.direction, self.moving_dir, self.action)

    def update_hit_box(self):

        while 0 < len(self.stand_box.other_name) and self.stand_box.is_on:
            o_name = self.stand_box.other_name.pop()
            o_type = self.stand_box.other_type.pop()
            o_pos = self.stand_box.other_center_pos.pop()
            o_range = self.stand_box.other_range.pop()
            o_range_pos = self.stand_box.other_range_pos.pop()
            o_edge_pos = self.stand_box.other_edge_pos.pop()
            stand = self.stand_box.hit.pop()

            if (
                    stand[POS.BOTTOM] and
                    not self.is_jump and
                    self.py >= o_range_pos[POS.TOP] + self.stand_box.range[POS.BOTTOM]
            ):

                if (
                        o_type == TYPE.PLATFORM_T or
                        o_type == TYPE.PLATFORM_NT
                ):
                    self.y = o_range_pos[POS.TOP] + self.stand_box.range[POS.BOTTOM]
                    self.full_jump()
                    self.gravity = 0
                    self.switch_fall(False)
                    self.switch_float(False)
                    self.reset_boxes_pos()

        while 0 < len(self.hit_box.other_name) and self.hit_box.is_on:
            o_name = self.hit_box.other_name.pop()
            o_type = self.hit_box.other_type.pop()
            o_pos = self.hit_box.other_center_pos.pop()
            o_range = self.hit_box.other_range.pop()
            o_range_pos = self.hit_box.other_range_pos.pop()
            o_edge_pos = self.hit_box.other_edge_pos.pop()
            hit = self.hit_box.hit.pop()

            if (
                    hit[POS.TOP] and
                    not hit[POS.BOTTOM] and
                    self.py <= o_range_pos[POS.BOTTOM] - self.hit_box.range[POS.TOP]
            ):
                self.y = o_range_pos[POS.BOTTOM] - self.hit_box.range[POS.TOP] - 1
                self.switch_fall()
                self.gravity = 0

            elif (
                    hit[POS.RIGHT] and
                    not hit[POS.LEFT] and
                    self.x < o_range_pos[POS.LEFT] and
                    self.hit_box.range_pos[POS.BOTTOM] < o_range_pos[POS.TOP]
            ):
                self.x = o_range_pos[POS.LEFT] - self.hit_box.range[POS.RIGHT]
                self.reset_boxes_pos()
                self.switch_stuck_r()

            elif (
                    hit[POS.LEFT] and
                    not hit[POS.RIGHT] and
                    self.x > o_range_pos[POS.RIGHT] and
                    self.hit_box.range_pos[POS.BOTTOM] < o_range_pos[POS.TOP]
            ):
                self.x = o_range_pos[POS.RIGHT] + self.hit_box.range[POS.LEFT]
                self.reset_boxes_pos()
                self.switch_stuck_l()

        if self.hit_box.is_on:
            if not self.is_jump and not self.hit_box.is_hit[POS.BOTTOM]:
                self.switch_fall()

            if (
                    (not self.hit_box.is_hit[POS.RIGHT]
                     or self.direction == D_LEFT)
            ):
                self.switch_stuck_r(False)

            if (
                    (not self.hit_box.is_hit[POS.LEFT]
                     or self.direction == D_RIGHT)
            ):
                self.switch_stuck_l(False)

        self.hit_box.is_hit = [False for b in range(len(self.hit_box.is_hit))]

        self.hit_box.set_pos(self.x, self.y)
        self.stand_box.set_pos(self.x, self.y)
        self.attack_box.set_pos(self.x, self.y)
        self.break_box.set_pos(self.x, self.y)

    def update(self):
        self.px, self.py = self.x, self.y
        self.update_state()
        # self.update_hit_box()
        self.update_move()
        self.update_animation()

    def handle_event(self, events):
        # events = get_events()

        for event in events:
            if event.type == SDL_QUIT:
                gs_framework.quit()

            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    return False

                elif event.key == SDLK_F3:
                    if self.is_show_hit_box:
                        self.is_show_hit_box = False
                    else:
                        self.is_show_hit_box = True

                elif event.key == SDLK_F2:
                    if self.is_show_object_box:
                        self.is_show_object_box = False
                    else:
                        self.is_show_object_box = True

                elif event.key == SDLK_RIGHT:
                    self.direction = D_RIGHT
                    self.moving_dir += D_RIGHT
                    self.switch_walk()
                elif event.key == SDLK_LEFT:
                    self.direction = D_LEFT
                    self.moving_dir += D_LEFT
                    self.switch_walk()
                elif event.key == SDLK_UP:
                    pass
                elif event.key == SDLK_DOWN:
                    if self.state != PS_SMALL:
                        self.switch_crawl()

                elif event.key == SDLK_z:
                    self.switch_run()
                elif event.key == SDLK_x:
                    if not self.is_fall:
                        self.switch_jump()

            elif event.type == SDL_KEYUP:

                if event.key == SDLK_RIGHT:
                    self.moving_dir += D_LEFT
                elif event.key == SDLK_LEFT:
                    self.moving_dir += D_RIGHT
                elif event.key == SDLK_UP:
                    pass
                elif event.key == SDLK_DOWN:
                    if self.state != PS_SMALL:
                        self.switch_crawl(False)

                elif event.key == SDLK_z:
                    self.switch_run(False)
                elif event.key == SDLK_x:
                    if self.is_jump and not self.is_fall:
                        self.switch_fall()
                        self.jump_power = 0

        return True
