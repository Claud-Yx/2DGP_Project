import game_object
import ob_player
from ob_background import *
from ob_map import *

from value import *

stage: Map
player: ob_player.Player
enemies = []
items = []
tiles = []
interactives = []
foreground = []
background: Background

start_time = 0.0
current_time = 0.0

time_stopper = []
time_stop = False

show_bb = False


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


def destroy():
    global stage, player, background, items

    del stage
    stage = None
    del player
    player = None
    del background
    background = None

    items.clear()
    enemies.clear()
    tiles.clear()
    interactives.clear()
    foreground.clear()


def move_camera(self: game_object.GameObject):
    global stage

    if isinstance(self, ob_player.Player):
        return

    self.rx = self.ax + stage.x
    self.ry = self.ay + stage.y
