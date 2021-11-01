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
    STAND = auto()
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


class OT( IntEnum ):  # Object Type
    TILESETS = 0
    ENEMIES = auto()
    ITMES = auto()
    INTERACTIVES = auto()
    SIZE = auto()


class EM( IntEnum ):  # Edit Menu
    MAIN = 0
    TILESETS = auto()
    ENEMIES = auto()
    ITMES = auto()
    INTERACTIVES = auto()
    BACKGROUNDS = auto()
    SIZE = auto()

class TID(IntEnum):  # Type ID
    GOOMBA = 0
    DRY_BONES = auto()
    BOO = auto()
    PIRANHA_PLANT = 10
    SPIKE_BALL = auto()
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
    LIFE_MUSHRUUM = auto()
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