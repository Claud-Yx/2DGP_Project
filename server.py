from ob_player import *
from ob_tileset import *
from ob_background import *
from ob_enemy import *

from value import *

player: Player
enemies: List[Enemy] = []
tiles: List[TileSet] = []
background: Background

start_time = 0.0
current_time = 0.0

time_stopper = []
time_stop = False


def stop_time(stop, *exceptob: Tuple[int, int]):
    global time_stopper, time_stop

    time_stop = stop

    if len(exceptob) == 0:
        time_stopper.clear()
        return

    for obj in exceptob:
        time_stopper.append(obj)

def init():
    global start_time, current_time
    global time_stopper, time_stop

    start_time = 0.0
    current_time = 0.0

    time_stopper = []
    time_stop = False