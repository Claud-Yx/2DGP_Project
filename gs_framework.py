from pico2d import *

Running = None
stack = None
Events = None
canvas_width = 1280
canvas_height = 720

frame_time = get_time()


def change_state(state):
    global stack
    global Threading

    if (len(stack) > 0):
        stack[-1].exit()
        stack.pop()

    stack.append(state)
    state.enter()


def push_state(state):
    global stack

    if (len(stack) > 0):
        stack[-1].pause()

    stack.append(state)
    state.enter()


def pop_state():
    global stack

    if (len(stack) > 0):
        stack[-1].exit()
        stack.pop()

    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global Running
    Running = False


def run(start_state):
    global Running, stack, Events, frame_time
    Running = True
    stack = [start_state]
    start_state.enter()
    current_time = get_time()

    while Running:
        Events = get_events()
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = get_time() - current_time
        if frame_time >= (1/60):
            frame_time = (1/60)
        current_time += frame_time

    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()
