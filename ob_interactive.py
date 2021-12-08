import gs_framework
from game_object import *


class WireMesh(GameObject, ABC):
    def __init__(self, lt_x, lt_y, rb_x, rb_y, dst_x=0, dst_y=0):

        lt_x = lt_x * 50 + 25
        lt_y = lt_y * 50 + 25
        rb_x = rb_x * 50 + 25
        rb_y = rb_y * 50 + 25

        self.index_x = (rb_x - lt_x) // ob_map.TILE_WIDTH + 1
        self.index_y = (lt_y - rb_y) // ob_map.TILE_HEIGHT + 1

        if self.index_x < 3 or self.index_y < 3:
            print("WireMesh Init Error")
            print("Index is too small: %d %d" % (self.index_x, self.index_y))
            exit(-1)

        # x = (rb_x - lt_x) / 2 + lt_x
        # y = (lt_y - rb_y) / 2 + rb_y

        x = lt_x
        y = rb_y

        super().__init__(TN.INTERACTIVES, TID.WIRE_MESH, x, y)

        self.px, self.py = 0.0, 0.0

        self.dst_x = self.ax + dst_x * 50
        self.dst_y = self.ay + dst_y * 50
        self.stp_x = self.ax
        self.stp_y = self.ay


        if dst_x == 0:
            self.is_move_x = False
            self.max_x_t = 0.0
        else:
            self.is_move_x = True
            self.max_x_t = abs(self.dst_x - self.stp_x) // 50 / 2

        if dst_y == 0:
            self.is_move_y = False
            self.max_y_t = 0.0
        else:
            self.is_move_y = True
            self.max_y_t = abs(self.dst_y - self.stp_y) // 50 / 2

        self.timer_move_x, self.timer_move_y = self.max_x_t, self.max_y_t

        self.tile = [[ACTION.PIECE_M for y in range(self.index_y)] for x in range(self.index_x)]

        for x in range(self.index_x):
            for y in range(self.index_y):
                if y == 0:
                    if x == 0:
                        self.tile[x][y] = ACTION.PIECE_LB
                    elif x == self.index_x - 1:
                        self.tile[x][y] = ACTION.PIECE_RB
                    else:
                        self.tile[x][y] = ACTION.PIECE_B
                elif y == self.index_y - 1:
                    if x == 0:
                        self.tile[x][y] = ACTION.PIECE_LT
                    elif x == self.index_x - 1:
                        self.tile[x][y] = ACTION.PIECE_RT
                    else:
                        self.tile[x][y] = ACTION.PIECE_T
                else:
                    if x == 0:
                        self.tile[x][y] = ACTION.PIECE_L
                    elif x == self.index_x - 1:
                        self.tile[x][y] = ACTION.PIECE_R

        self.got_player = False

    def update(self):
        if self.is_time_stop:
            return

        self.init_bb()
        self.set_bb_size()

        if self.is_move_x:
            if self.timer_move_x == 0:
                self.timer_move_x = self.max_x_t
                self.dst_x, self.stp_x = self.stp_x, self.dst_x

            self.px = self.ax
            self.ax = self.timer_move_x/self.max_x_t * self.stp_x + (1 - self.timer_move_x/self.max_x_t) * self.dst_x
            self.timer_move_x -= gs_framework.frame_time
            if self.timer_move_x <= 0:
                self.timer_move_x = 0
            if self.got_player:
                server.player.ax += (self.ax - self.px)


    def draw(self):
        server.move_camera(self)

        for x in range(self.index_x):
            for y in range(self.index_y):

                # if self.frame_count == 1:
                #     self.frame = 0

                self.set_clip(self.tile[x][y])
                GameObject.image[self.type_name, self.type_id].clip_draw(
                    int(self.frame_begin) * self.l, self.b, self.w, self.h,
                    self.rx + x * ob_map.TILE_WIDTH, self.ry + y * ob_map.TILE_HEIGHT
                )
                # print("drew (%.2f, %.2f): %s" %
                #       (self.x + x * ob_map.TILE_WIDTH, self.y + y * ob_map.TILE_HEIGHT, self.tile[x][y])

        if self.show_bb:
            self.draw_bb()

    def handle_event(self, event):
        pass



