import gs_framework
from pico2d import *

import gs_loading

name = "StartLogoState"

logo = None
effect_fade = None
logo_time = 0.0


def enter():
    global logo
    global effect_fade
    global logo_time

    logo = load_image('resource\\logo_image\\title_logo.png')
    effect_fade = load_image('resource\\effect\\fade_black.png')
    logo_time = 0.0


def exit():
    global logo
    global effect_fade

    del logo
    del effect_fade


def handle_events():
    Events = gs_framework.Events

    for event in Events:
        if event.type == SDL_QUIT:
            gs_framework.quit()


def update():
    global logo_time

    if (logo_time > 3.0):
        logo_time = 0
        gs_framework.change_state(gs_loading)
        gs_framework.stack[-1].update()
        return
    delay(0.01)
    logo_time += 0.01


def draw():
    global logo
    global effect_fade
    global logo_time

    clear_canvas()

    if logo_time <= 0.1:
        effect_fade.clip_draw(19, 0, 1, 1,
                              pico2d.get_canvas_width()//2, pico2d.get_canvas_height()//2,
                              pico2d.get_canvas_width(), pico2d.get_canvas_height())

    logo.draw(pico2d.get_canvas_width()//2, pico2d.get_canvas_height()//2)

    if logo_time <= 0.5:
        effect_fade.clip_draw(19, 0, 1, 1,
                              pico2d.get_canvas_width()//2, pico2d.get_canvas_height()//2,
                              pico2d.get_canvas_width(), pico2d.get_canvas_height())

    elif logo_time <= 1.0:
        ran = logo_time - 0.5
        frame = int(19 - ran * 100)
        if frame >= 0:
            effect_fade.clip_draw(frame, 0, 1, 1,
                                  pico2d.get_canvas_width()//2, pico2d.get_canvas_height()//2,
                                  pico2d.get_canvas_width(), pico2d.get_canvas_height())

    elif logo_time <= 2.5:
        ran = logo_time - 2.3
        frame = int(0 + ran * 100)
        if frame >= 0:
            effect_fade.clip_draw(frame, 0, 1, 1,
                                  pico2d.get_canvas_width()//2, pico2d.get_canvas_height()//2,
                                  pico2d.get_canvas_width(), pico2d.get_canvas_height())

    elif logo_time > 2.5:
        effect_fade.clip_draw(19, 0, 1, 1,
                              pico2d.get_canvas_width()//2, pico2d.get_canvas_height()//2,
                              pico2d.get_canvas_width(), pico2d.get_canvas_height())

    update_canvas()

def pause():
    pass

def resume():
    pass


def test_gs_start_logo():
    global logo
    global logo_time
    global effect_fade

    open_canvas(gs_framework.canvas_width, gs_framework.canvas_height)

    enter()

    while logo_time < 3.0:

        Events = get_events()

        for event in Events:
            if event.type_id == SDL_QUIT:
                logo_time = 4

        update()
        draw()

    close_canvas()

    return True


if __name__ == "__main__":
    print("== gs_start_logo.py is prepared.")
    print("== start testing gs_start_logo.py\n")
    if test_gs_start_logo():
        print("\n== testing gs_start_logo.py is done.")
    else:
        print("\n== error: testing gs_start_logo.py is crashed")


