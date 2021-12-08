
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

        self.dst_x = dst_x
        self.dst_y = dst_y
        self.stp_x = self.ax
        self.stp_y = self.ay

        if self.dst_x == 0:
            self.is_move_x = False
            self.x_direction = DIR.NONE
        else:
            self.is_move_x = True
            if self.dst_x > 0:
                self.x_direction = DIR.RIGHT
            else:
                self.x_direction = DIR.LEFT

        if self.dst_y == 0:
            self.is_move_y = False
            self.y_direction = DIR.NONE
        else:
            self.is_move_y = True
            if self.dst_y > 0:
                self.y_direction = DIR.UP
            else:
                self.y_direction = DIR.DOWN


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



