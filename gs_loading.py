from pico2d import *
import gs_framework
import gs_title

import stage_manager

name = "StageLoading"

bg = None
loading = None

def enter():
    global bg, loading
    if bg is None:
        bg = load_image("resource\\effect\\fade_black.png")

    loading = load_font('resource\\font\\new_super_mario_font.ttf', 50)

def exit():
    pass

def handle_events():
    for event in gs_framework.Events:
        if event.type == SDL_QUIT:
            gs_framework.quit()

def update():
    # stage_manager.stage = {(1,1): stage_manager.Stage(
    #     "%ss%.2d%.2d%s" % (stage_manager.FILE_PATH, 1, 1, stage_manager.FILE_FORMAT))
    # }
    # print("sm update")
    pass

def draw():
    global bg, loading

    clear_canvas()

    bg.clip_draw(19, 0, 1, 1,
                 gs_framework.canvas_width // 2, gs_framework.canvas_height // 2,
                 gs_framework.canvas_width, gs_framework.canvas_height)

    loading.draw(50, 50, "Now Loading...", (255, 255, 255))

    update_canvas()

    delay(1)

    gs_framework.change_state(gs_title)

def pause():
    pass

def resume():
    pass