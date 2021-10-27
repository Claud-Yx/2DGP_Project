from pico2d import *

Running = None
stack = None
Events = None
canvas_width = 1280
canvas_height = 720


def change_state(state):
    global stack

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
    global Running, stack, Events
    Running = True
    stack = [start_state]
    start_state.enter()

    while Running:
        Events = get_events()
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()