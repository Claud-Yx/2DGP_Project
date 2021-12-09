import game_object
import ob_background
import ob_player
import object_manager

from value import *

stage = None
player = None
enemies = []
items = []
tiles = []
interactives = []
foreground = []
background = None

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

    object_manager.objects = [[], [], [], [], []]


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


def move_bg(self: ob_background.Background):
    global stage

    self.bx = stage.x * 0.3
    self.by = stage.y * 0.3

    self.fx = stage.x * 0.8
    self.fy = stage.y * 0.8
