from enum import Enum, IntEnum, auto
from typing import List, Set, Dict, Tuple

GRAVITY_ACCEL_MPS = 9.8
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm


def get_pps_from_kmph(kmph):
    return kmph * 1000.0 / 3600.0 * PIXEL_PER_METER


def get_pps_from_mps(mps):
    return mps * PIXEL_PER_METER


def get_accel_from_pps(pps, t):
    if t == 0:
        print("cannot divide by 0")
        return None

    return pps / t


GRAVITY_ACCEL_PPS = get_pps_from_mps(GRAVITY_ACCEL_MPS)


# class StrEnum(str, Enum):
#     def _generate_next_value_(name, start, count, last_values):
#         return name
#
#     def __str__(self):
#         return self.name

# class NAME(StrEnum):
#     PLAYER_SMALL = auto()
#     PLAYER_SUPER = auto()
#     ENEMY = auto()
#     INTERACTIVE = auto()
#     ITEM = auto()
#     TILESET = auto()
#
#
# class TYPE(StrEnum):
#     HIT = auto()
#     STAND = auto()
#     ATTACK = auto()
#     BREAK = auto()
#
#     GOOMBA = auto()
#     DRY_BONES = auto()
#
#     WIRE_MESH = auto()
#     DOOR = auto()
#
#     SUPER_MUSHROOM = auto()
#
#     PLATFORM_T = auto()
#     PLATFORM_NT = auto()
#     PIPE = auto()


class DIR(IntEnum):
    NONE = 0
    LEFT = -1
    RIGHT = 1
    UP = 1
    DOWN = -1


class POS(IntEnum):
    LEFT = 0
    BOTTOM = 1
    RIGHT = 2
    TOP = 3

    X = 0
    Y = 1


class ACTION(IntEnum):
    IDLE = 0
    SIT = auto()
    WALK = auto()
    RUN = auto()
    BREAK = auto()
    FLY = auto()
    JUMP = auto()
    FALL = auto()
    HANG = auto()
    CLIMB = auto()
    SWIM = auto()
    RESTORE = auto()
    ATTACK = auto()
    DIE_A = auto()
    DIE_B = auto()


class TN(IntEnum):  # Object Type
    PLAYER = 0
    TILESETS = auto()
    ENEMIES = auto()
    ITEMS = auto()
    INTERACTIVES = auto()
    FOREGROUND = auto()
    SIZE = auto()
    NONE = 99


class EM(IntEnum):  # Edit Menu
    MAIN = 0
    TILESETS = auto()
    ENEMIES = auto()
    ITMES = auto()
    INTERACTIVES = auto()
    BACKGROUNDS = auto()
    SIZE = auto()


class TID(IntEnum):  # Type ID
    MARIO_SMALL = 0
    MARIO_SUPER = auto()
    MARIO_FLAME = auto()

    GOOMBA = 0
    DRY_BONES = auto()
    BOO = auto()
    PIRANHA_PLANT = 10
    SPINNING_SPIKE = auto()
    BOSS = 20

    DOOR_RG = 0
    DOOR_BS = 1

    PIPE_UP = 0
    PIPE_DOWN = auto()
    PIPE_LEFT = auto()
    PIPE_RIGHT = auto()

    CASTLE_BLOCK_50X50 = 0
    CASTLE_BLOCK_50X100 = auto()
    CASTLE_BLOCK_100X50 = auto()
    CASTLE_BLOCK_100X100 = auto()

    COIN = 0
    SUPER_MUSHROOM = auto()
    LIFE_MUSHROOM = auto()
    FIRE_FLOWER = auto()
    SUPER_STAR = auto()
    STAR_COIN = auto()

    BREAKABLE_BRICK = 0
    UNBREAKABLE_BRICK = auto()
    RANDOM_BOX = auto()
    PLAT_FORM = auto()
    SPIKE_UP = 10
    SPIKE_DOWN = auto()
    SPIKE_LEFT = auto()
    SPIKE_RIGHT = auto()
    WIRE_MESH = auto()

    NONE = 99


class HB(IntEnum):  # Hit box
    BODY = 0
    LEFT = auto()
    BOTTOM = auto()
    TOP = auto()
    RIGHT = auto()
    ATTACK = auto()
    BREAK = auto()
    SIZE = auto()


class L(IntEnum):  # Layer
    BACKGROUND = 0
    PLAYER = 3
    TILESETS = 2
    ENEMIES = 3
    ITEMS = 3
    INTERACTIVES = 1
    FOREGROUND = 4


class Numbering:
    number = 0

    def nbr(self=None, begin=False):
        if begin:
            Numbering.number = 0

        temp = Numbering.number
        Numbering.number += 1

        return temp


def nbr(begin=False):
    return Numbering.nbr(begin=begin)
