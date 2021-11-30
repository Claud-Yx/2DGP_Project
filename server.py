from ob_background import *
from ob_map import *

from value import *

stage: Map
player: Player
enemies = []
items = []
tiles = []
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


def destroy():
    global stage, player, background, items

    del stage
    del player
    del background
    items.clear()
    enemies.clear()
    tiles.clear()


def move_camera_x(self: game_object.GameObject):
    global player, stage

    if (server.player.x == gs_framework.canvas_width // 2 + 50 or
            server.player.x == gs_framework.canvas_width // 2 - 50
    ):
        self.x -= server.player.velocity * gs_framework.frame_time
