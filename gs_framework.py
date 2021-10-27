from pico2d import *

Running = None
stack = None
Events = None
Threading = True
canvas_width = 1280
canvas_height = 720


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
    global Running, stack, Events
    Running = True
    Threading = True
    stack = [start_state]
    start_state.enter()

    while Running:
        if stack[-1].name == "StageMainState" and Threading:
            stack[-1].UpdateFrameThd.start()
            Threading = False
        elif not stack[-1].name == "StageMainState" and not Threading:
            Threading = True

        Events = get_events()
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()