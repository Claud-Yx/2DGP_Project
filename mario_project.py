from pico2d import *
import gs_framework

# import gs_start_logo
import gs_stage_main

open_canvas(gs_framework.canvas_width, gs_framework.canvas_height)
load_image('resource\\effect\\fade_black.png').clip_draw(19, 0, 1, 1,
    gs_framework.canvas_width//2, gs_framework.canvas_height//2,
    gs_framework.canvas_width, gs_framework.canvas_height
    )
update_canvas()
# delay(3.0)
gs_framework.run(gs_stage_main)
close_canvas()