from enum import auto, IntEnum
from value import *
import pico2d


class HitBox:
    image = None

    def __init__(self, x, y, yt=10, yb=10, xl=10, xr=10, on=True,
                 img_path='resource\\hit_box.png', img_id=2, name="", type=""):

        # Hit box info
        self.name = name
        self.type = type

        # Hit other box info
        self.other_name = [""]
        self.other_type = [""]
        self.other_center_pos = [[0, 0]]
        self.other_range = [[0, 0, 0, 0]]
        self.other_range_pos = [[0, 0, 0, 0]]
        self.other_edge_pos = [[[0, 0], [0, 0], [0, 0], [0, 0]]]

        # Hit box center position
        self.center_pos = [x, y]

        # Hit box range
        self.range = [yt, yb, xl, xr]

        # Hit box position range
        self.range_pos = [y + self.range[POS.TOP], y - self.range[POS.BOTTOM],
                          x - self.range[POS.LEFT], x + self.range[POS.RIGHT]]

        # Hit box edge position
        self.edge_pos = [[self.range_pos[POS.LEFT], self.range_pos[POS.TOP]],
                         [self.range_pos[POS.LEFT], self.range_pos[POS.BOTTOM]],
                         [self.range_pos[POS.RIGHT], self.range_pos[POS.TOP]],
                         [self.range_pos[POS.RIGHT], self.range_pos[POS.BOTTOM]]]

        # Hit box checking
        self.hit = [[False for b in range(4)]]
        self.is_on = on
        self.is_hit = [False for b in range(4)]

        # Hit box image
        if img_path == '':
            self.image = None
        else:
            self.image = pico2d.load_image(img_path)
        self.image_id = img_id  # 0:blue / 1:green / 2:red

    def set_info(self, n="", t=""):
        self.name = n
        self.type = t

    def get_info(self):
        return [self.name, self.type]

    def set_other_info(self, name="", type="", pos=[], range=[], r_pos=[], e_pos=[]):
        self.other_name.append(name)
        self.other_type.append(type)
        self.other_center_pos.append(pos)
        self.other_range.append(range)
        self.other_range_pos.append(r_pos)
        self.other_edge_pos.append(e_pos)

    def get_other_info(self):
        return [self.other_name, self.other_type]

    def set_pos(self, x, y):
        self.center_pos = [x, y]
        self.reset_pos_range()
        self.reset_edge_pos()

    def set_range(self, yt, yb, xl, xr):
        self.range = [yt, yb, xl, xr]
        self.reset_pos_range()
        self.reset_edge_pos()

    def reset_pos_range(self):
        self.range_pos = [self.center_pos[POS.Y] + self.range[POS.TOP],
                          self.center_pos[POS.Y] - self.range[POS.BOTTOM],
                          self.center_pos[POS.X] - self.range[POS.LEFT],
                          self.center_pos[POS.X] + self.range[POS.RIGHT]]

    def reset_edge_pos(self):
        self.edge_pos = [[self.range_pos[POS.LEFT], self.range_pos[POS.TOP]],
                         [self.range_pos[POS.LEFT], self.range_pos[POS.BOTTOM]],
                         [self.range_pos[POS.RIGHT], self.range_pos[POS.TOP]],
                         [self.range_pos[POS.RIGHT], self.range_pos[POS.BOTTOM]]]

    def is_pos_in_box(self, pos, x=0, y=0, t=0, b=0, l=0, r=0):
        if self.range_pos[POS.TOP] + t >= pos[POS.Y] + y >= self.range_pos[POS.BOTTOM] - b:
            if self.range_pos[POS.LEFT] - l <= pos[POS.X] + x <= self.range_pos[POS.RIGHT] + r:
                return True
        return False

    def check_hit(self, other, adj = -1):
        hit = [False for b in range(4)]

        # top check
        if self.is_on:
            if (
                    other.is_pos_in_box(self.edge_pos[POS.LT], t=adj, l=adj, r=adj) or
                    other.is_pos_in_box(self.edge_pos[POS.RT], t=adj, l=adj, r=adj) or
                    self.is_pos_in_box(other.edge_pos[POS.LB], b=adj, l=adj, r=adj) or
                    self.is_pos_in_box(other.edge_pos[POS.RB], b=adj, l=adj, r=adj)
            ):
                hit[POS.TOP] = True
                self.is_hit[POS.TOP] = True

            # bottom check
            if (
                    other.is_pos_in_box(self.edge_pos[POS.LB], b=adj, l=adj, r=adj) or
                    other.is_pos_in_box(self.edge_pos[POS.RB], b=adj, l=adj, r=adj) or
                    self.is_pos_in_box(other.edge_pos[POS.LT], t=adj, l=adj, r=adj) or
                    self.is_pos_in_box(other.edge_pos[POS.RT], t=adj, l=adj, r=adj)
            ):
                hit[POS.BOTTOM] = True
                self.is_hit[POS.BOTTOM] = True

            # left check
            if (
                    other.is_pos_in_box(self.edge_pos[POS.LT], t=adj, b=adj, l=adj) or
                    other.is_pos_in_box(self.edge_pos[POS.LB], t=adj, b=adj, l=adj) or
                    self.is_pos_in_box(other.edge_pos[POS.RT], t=adj, b=adj, r=adj) or
                    self.is_pos_in_box(other.edge_pos[POS.RB], t=adj, b=adj, r=adj)
            ):
                hit[POS.LEFT] = True
                self.is_hit[POS.LEFT] = True

            # left check
            if (
                    other.is_pos_in_box(self.edge_pos[POS.RT], t=adj, b=adj, r=adj) or
                    other.is_pos_in_box(self.edge_pos[POS.RB], t=adj, b=adj, r=adj) or
                    self.is_pos_in_box(other.edge_pos[POS.LT], t=adj, b=adj, l=adj) or
                    self.is_pos_in_box(other.edge_pos[POS.LB], t=adj, b=adj, l=adj)
            ):
                hit[POS.RIGHT] = True
                self.is_hit[POS.RIGHT] = True

            # return check
            for b in hit:
                if b:
                    self.hit.append(hit)
                    self.set_other_info(other.name, other.type,
                                        other.center_pos, other.range,
                                        other.range_pos, other.edge_pos)
                    return True
        return False

    def show_hit_box(self):
        if self.is_on:
            for x in range(self.edge_pos[POS.LT][POS.X], self.edge_pos[POS.RT][POS.X] + 1):
                self.image.clip_draw(0, self.image_id, 1, 1, x, self.range_pos[POS.TOP])
                self.image.clip_draw(0, self.image_id, 1, 1, x, self.range_pos[POS.BOTTOM])

            for y in range(self.edge_pos[POS.LB][POS.Y], self.edge_pos[POS.LT][POS.Y] + 1):
                self.image.clip_draw(0, self.image_id, 1, 1, self.range_pos[POS.LEFT], y)
                self.image.clip_draw(0, self.image_id, 1, 1, self.range_pos[POS.RIGHT], y)


def test_hit_box():
    if __name__ != "__main__":
        return False

    import os

    def handle_event(pos):

        events = pico2d.get_events()

        for event in events:
            if event.type == pico2d.SDL_QUIT:
                return False

            elif event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_ESCAPE:
                    return False

            elif event.type == pico2d.SDL_MOUSEMOTION:
                pos[0], pos[1] = event.X, 600 - 1 - event.Y

        return True

    def update_hit_check(a, b):
        a.check_hit(b)
        b.check_hit(a)

        bl = ""

        debug_a = [pico2d.load_font(os.getenv('PICO2D_DATA_PATH') + '/ConsolaMalgun.TTF') for i in range(4)]
        debug_b = [pico2d.load_font(os.getenv('PICO2D_DATA_PATH') + '/ConsolaMalgun.TTF') for i in range(4)]

        direction = ["Top", "Bottom", "Left", "Right"]
        for i in range(4):
            if a.hit[i]:
                bl = "True"
            else:
                bl = "False"
            debug_a[i].draw(10, 600 - (i * 30 + 10), "small box [" + direction[i] + "]: " + bl, (0, 0, 100))

            if b.hit[i]:
                bl = "True"
            else:
                bl = "False"
            debug_b[i].draw(10, 600 - (i * 30 + 130), "big box [" + direction[i] + "]: " + bl, (0, 0, 100))

        debug_a_info = [pico2d.load_font(os.getenv('PICO2D_DATA_PATH') + '/ConsolaMalgun.TTF') for i in range(4)]
        debug_b_info = [pico2d.load_font(os.getenv('PICO2D_DATA_PATH') + '/ConsolaMalgun.TTF') for i in range(4)]

        x = 400

        debug_a_info[0].draw(pico2d.get_canvas_width() - x,
                             pico2d.get_canvas_height() - 10,
                             "small box name: " + a.name, (0, 0, 100))
        debug_a_info[1].draw(pico2d.get_canvas_width() - x,
                             pico2d.get_canvas_height() - 40,
                             "small box type: " + a.type, (0, 0, 100))
        debug_a_info[2].draw(pico2d.get_canvas_width() - x,
                             pico2d.get_canvas_height() - 70,
                             "small box other name: " + a.other_name, (0, 0, 100))
        debug_a_info[3].draw(pico2d.get_canvas_width() - x,
                             pico2d.get_canvas_height() - 100,
                             "small box other type: " + a.other_type, (0, 0, 100))

        debug_b_info[0].draw(pico2d.get_canvas_width() - x,
                             pico2d.get_canvas_height() - 130,
                             "big box name: " + b.name, (0, 0, 100))
        debug_b_info[1].draw(pico2d.get_canvas_width() - x,
                             pico2d.get_canvas_height() - 160,
                             "big box type: " + b.type, (0, 0, 100))
        debug_b_info[2].draw(pico2d.get_canvas_width() - x,
                             pico2d.get_canvas_height() - 190,
                             "big box other name: " + b.other_name, (0, 0, 100))
        debug_b_info[3].draw(pico2d.get_canvas_width() - x,
                             pico2d.get_canvas_height() - 220,
                             "big box other type: " + b.other_type, (0, 0, 100))

    Running = True

    print("= enum class Pos")
    print(POS.__itemsize__)

    for pos in POS:
        print(pos, "=", pos.value)
    print()

    hb = HitBox(50, 50, img_path='')
    print("= Created: initialized test HitBox class - hb")

    print("hb.name:", hb.name, "| hb.type:", hb.type)
    print("hb.center_pos:", hb.center_pos)

    print("hb.range:", hb.range)
    print("hb.pos_range:", hb.range_pos)
    print("hb.edge_pos:", hb.edge_pos)
    print()

    print("= open canvas")
    pico2d.open_canvas()

    object_x, object_y = 400, 300
    object_hit_box = HitBox(object_x, object_y, 50, 50, 50, 50)
    object_hit_box.set_info("big_box", "tile_set")
    object = pico2d.load_image('resource\\tileset\\block100x100.png')

    mpos = [50, 50]
    mouse_hit_box = HitBox(mpos[0], mpos[1], 25, 25, 25, 25)
    mouse_hit_box.set_info("small_box", "moving_tile")
    mouse_object = pico2d.load_image('resource\\tileset\\block50x50.png')

    pico2d.hide_cursor()
    pico2d.hide_lattice()

    while Running:
        pico2d.clear_canvas()

        object.draw(object_x, object_y)
        mouse_object.draw(mpos[0], mpos[1])
        update_hit_check(mouse_hit_box, object_hit_box)

        object_hit_box.show_hit_box()
        mouse_hit_box.show_hit_box()

        pico2d.update_canvas()

        Running = handle_event(mpos)
        mouse_hit_box.set_pos(mpos[0], mpos[1])
        pico2d.delay(0.01)

    pico2d.close_canvas()

    return True


if __name__ == "__main__":
    print("== hit_box.py is prepared.")
    print("== start testing hit_box.py\n")
    if test_hit_box():
        print("\n== testing hit_box.py is done.")
    else:
        print("\n== error: testing hit_box.py is crashed")
