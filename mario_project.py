from pico2d import *
import gs_framework

import gs_start_logo

open_canvas(gs_framework.canvas_width, gs_framework.canvas_height)
load_image('resource\\effect\\fade_black.png').draw_now(
    gs_framework.canvas_width//2, gs_framework.canvas_height//2,
    gs_framework.canvas_width, gs_framework.canvas_height
    )
gs_framework.run(gs_start_logo)
close_canvas()