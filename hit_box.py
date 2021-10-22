from enum import auto, IntEnum
import pico2d


class Pos( IntEnum ):
    top = 0
    bottom = auto()
    left = auto()
    right = auto()

    lefttop = 0
    leftbottom = auto()
    righttop = auto()
    rightbottom = auto()

    lt = 0
    lb = auto()
    rt = auto()
    rb = auto()

    x = 0
    y = 1


class HitBox:
    def __init__( self, x, y, yt = 10, yb = 10, xl = 10, xr = 10, on = True,
                  img_path='resource\\hit_box.png', img_id=2):
        # Hit box name
        self.name = ""
        self.type = ""

        # Hit box center position
        self.center_pos = [x, y]

        # Hit box range
        self.range = [ yt, yb, xl, xr ]

        # Hit box position range
        self.pos_range = [ y + self.range[ Pos.top ], y - self.range[ Pos.bottom ],
                           x - self.range[ Pos.left ], x + self.range[ Pos.right ] ]

        # Hit box edge position
        self.edge_pos = [ [self.pos_range[Pos.left], self.pos_range[Pos.top]],
                          [self.pos_range[Pos.left], self.pos_range[Pos.bottom]],
                          [self.pos_range[Pos.right], self.pos_range[Pos.top]],
                          [self.pos_range[Pos.right], self.pos_range[Pos.bottom]]]

        # Hit box checking
        self.is_hit = [False for b in range(4)]
        self.is_on = on

        # Hit box image
        if img_path == '':
            self.image = None
        else:
            self.image = pico2d.load_image(img_path)
        self.image_id = img_id  # 0:blue / 1:green / 2:red

    def set_pos( self, x, y ):
        self.center_pos = [x, y]
        self.reset_pos_range()
        self.reset_edge_pos()

    def set_range( self, yt, yb, xl, xr ):
        self.range = [yt, yb, xl, xr]
        self.reset_pos_range()
        self.reset_edge_pos()

    def reset_pos_range( self ):
        self.pos_range = [ self.center_pos[Pos.y] + self.range[Pos.top],
                           self.center_pos[Pos.y] - self.range[Pos.bottom],
                           self.center_pos[Pos.x] - self.range[Pos.left],
                           self.center_pos[Pos.x] + self.range[Pos.right]]

    def reset_edge_pos( self ):
        self.edge_pos = [ [self.pos_range[Pos.left], self.pos_range[Pos.top]],
                          [self.pos_range[Pos.left], self.pos_range[Pos.bottom]],
                          [self.pos_range[Pos.right], self.pos_range[Pos.top]],
                          [self.pos_range[Pos.right], self.pos_range[Pos.bottom]]]

    def is_pos_in_box( self, pos, x=0, y=0, t=0, b=0, l=0, r=0 ):
        if self.pos_range[Pos.top] + t >= pos[Pos.y] + y >= self.pos_range[Pos.bottom] - b:
            if self.pos_range[Pos.left] - l <= pos[Pos.x] + x <= self.pos_range[Pos.right] + r:
                return True
        return False

    def check_hit( self, other ):

        # top check
        if self.is_on:
            if (
                    other.is_pos_in_box(self.edge_pos[Pos.lt], t=-1, l=-1, r=-1) or
                    other.is_pos_in_box(self.edge_pos[Pos.rt], t=-1, l=-1, r=-1) or
                    self.is_pos_in_box(other.edge_pos[Pos.lb], b=-1, l=-1, r=-1) or
                    self.is_pos_in_box(other.edge_pos[Pos.rb], b=-1, l=-1, r=-1)
            ):
                self.is_hit[Pos.top] = True
            else:
                self.is_hit[Pos.top] = False

            # bottom check
            if (
                    other.is_pos_in_box( self.edge_pos[ Pos.lb ], b=-1, l=-1, r=-1 ) or
                    other.is_pos_in_box( self.edge_pos[ Pos.rb ], b=-1, l=-1, r=-1 ) or
                    self.is_pos_in_box( other.edge_pos[ Pos.lt ], t=-1, l=-1, r=-1 ) or
                    self.is_pos_in_box( other.edge_pos[ Pos.rt ], t=-1, l=-1, r=-1 )
            ):
                self.is_hit[Pos.bottom] = True
            else:
                self.is_hit[Pos.bottom] = False

            # left check
            if (
                    other.is_pos_in_box( self.edge_pos[ Pos.lt ], t=-1, b=-1, l=-1 ) or
                    other.is_pos_in_box( self.edge_pos[ Pos.lb ], t=-1, b=-1, l=-1 ) or
                    self.is_pos_in_box( other.edge_pos[ Pos.rt ], t=-1, b=-1, r=-1 ) or
                    self.is_pos_in_box( other.edge_pos[ Pos.rb ], t=-1, b=-1, r=-1 )
            ):
                self.is_hit[Pos.left] = True
            else:
                self.is_hit[Pos.left] = False

            # left check
            if (
                    other.is_pos_in_box( self.edge_pos[ Pos.rt ], t=-1, b=-1, r=-1 ) or
                    other.is_pos_in_box( self.edge_pos[ Pos.rb ], t=-1, b=-1, r=-1 ) or
                    self.is_pos_in_box( other.edge_pos[ Pos.lt ], t=-1, b=-1, l=-1 ) or
                    self.is_pos_in_box( other.edge_pos[ Pos.lb ], t=-1, b=-1, l=-1 )
            ):
                self.is_hit[Pos.right] = True
            else:
                self.is_hit[Pos.right] = False

            # return check
            for b in self.is_hit:
                if b:
                    return True
        return False

    def get_info( self ):
        return [self.name, self.type]

    def show_hit_box( self ):
        if self.is_on:
            for x in range(self.edge_pos[Pos.lt][Pos.x], self.edge_pos[Pos.rt][Pos.x]+1):
                self.image.clip_draw(0, self.image_id, 1, 1, x, self.pos_range[Pos.top])
                self.image.clip_draw(0, self.image_id, 1, 1, x, self.pos_range[Pos.bottom])

            for y in range(self.edge_pos[Pos.lb][Pos.y], self.edge_pos[Pos.lt][Pos.y]+1):
                self.image.clip_draw(0, self.image_id, 1, 1, self.pos_range[Pos.left], y)
                self.image.clip_draw(0, self.image_id, 1, 1, self.pos_range[Pos.right], y)


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
                pos[0], pos[1] = event.x, 600 - 1 - event.y

        return True

    def update_hit_check(a, b):
        a.check_hit(b)
        b.check_hit(a)

        bl = ""

        debug_a = [pico2d.load_font(os.getenv('PICO2D_DATA_PATH') + '/ConsolaMalgun.TTF') for i in range(4)]
        debug_b = [pico2d.load_font(os.getenv('PICO2D_DATA_PATH') + '/ConsolaMalgun.TTF') for i in range(4)]

        direction = ["Top", "Bottom", "Left", "Right"]
        for i in range(4):
            if a.is_hit[i]:
                bl = "True"
            else:
                bl = "False"
            debug_a[i].draw(10, 600 - (i*30+30), "small box [" + direction[i] + "]: " + bl, (0, 0, 100))

            if b.is_hit[i]:
                bl = "True"
            else:
                bl = "False"
            debug_b[i].draw(10, 600-(i*30+160), "big box [" + direction[i] + "]: " + bl, (0, 0, 100))

    Running = True

    print("= enum class Pos")
    print(Pos.__itemsize__)

    for pos in Pos:
        print( pos, "=", pos.value)
    print()

    hb = HitBox( 50, 50, img_path = '' )
    print("= Created: initialized test HitBox class - hb")

    print("hb.name:", hb.name, "| hb.type:", hb.type)
    print("hb.center_pos:", hb.center_pos)

    print("hb.range:", hb.range)
    print("hb.pos_range:", hb.pos_range )
    print("hb.edge_pos:", hb.edge_pos)
    print()

    print("= open canvas")
    pico2d.open_canvas()

    object_x, object_y = 400, 300
    object_hit_box = HitBox(object_x, object_y, 50, 50, 50, 50)
    object = pico2d.load_image('resource\\tileset\\block100x100.png')

    mpos = [ 50, 50 ]
    mouse_hit_box = HitBox(mpos[0], mpos[1], 25, 25, 25, 25)
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
    print( "== hit_box.py is prepared." )
    print("== start testing hit_box.py\n")
    if test_hit_box():
        print( "\n== testing hit_box.py is done." )
    else:
        print( "\n== error: testing hit_box.py is crashed" )
