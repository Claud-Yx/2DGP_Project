from enum import Enum, IntEnum, auto


class StrEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self.name


class NAME(StrEnum):
    PLAYER_SMALL = auto()
    PLAYER_SUPER = auto()
    ENEMY = auto()
    INTERACTIVE = auto()
    ITEM = auto()
    TILESET = auto()


class TYPE(StrEnum):
    HIT = auto()
    ATTACK = auto()
    BREAK = auto()

    GOOMBA = auto()
    DRY_BONES = auto()

    WIRE_MESH = auto()
    DOOR = auto()

    SUPER_MUSHROOM = auto()

    PLATFORM_T = auto()
    PLATFORM_NT = auto()
    PIPE = auto()


class POS( IntEnum ):
    TOP = 0
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()

    LEFTTOP = 0
    LEFTBOTTOM = auto()
    RIGHTTOP = auto()
    RIGHTBOTTOM = auto()

    LT = 0
    LB = auto()
    RT = auto()
    RB = auto()

    X = 0
    Y = 1


