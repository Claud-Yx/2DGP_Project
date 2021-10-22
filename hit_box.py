from pico2d import *
from enum import Enum, auto, IntEnum


class Pos(IntEnum):
    top = 0
    bottom = auto()
    left = auto()
    right = auto()


class HitBox:
    def __init__(self, x, y):
        # Hit box name
        self.name = ""
        self.type = ""

        # Hit box range
        self.range = [0, 0, 0, 0]

        # Hit box pos
        self.pos = [y + self.range[Pos.top], y - self.range[Pos.bottom],
                    x - self.range[Pos.left], x + self.range[Pos.right] ]


def test_hit_box():

    hb = HitBox(50, 50)

    print(hb.range)
    for pos in Pos:
        print(pos.value)

    open_canvas()


    clear_canvas()
    update_canvas()
    delay(3)

    close_canvas()


if __name__ == "__main__":
    print( "hit_box is prepared." )
    test_hit_box()
    print( "testing hit_box is done." )