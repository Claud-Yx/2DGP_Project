from pico2d import *
import gs_framework

import gs_stage_enter

logo = None
menu = []
menu_outline = []
cursor = None
cursor_pos = [gs_framework.canvas_width // 2 - 200, gs_framework.canvas_height // 2]
menu_index = 0


def enter():
    global logo
    global menu
    global menu_outline
    global cursor

    logo = load_image('resource\\logo_image\\title.png')
    menu = [load_font('resource\\font\\new_super_mario_font.ttf', 50) for i in range(3)]
    menu_outline = [load_font('resource\\font\\new_super_mario_font_outline.ttf', 50) for i in range(3)]
    cursor = load_image('resource\\logo_image\\cursor.png')


def exit():
    global logo
    global menu, menu_index
    global menu_outline
    global cursor, cursor_pos

    del logo
    del menu
    del menu_outline
    del cursor
    del cursor_pos
    del menu_index


def handle_events():
    global menu_index

    Events = gs_framework.Events

    for event in Events:
        if event.type == SDL_QUIT:
            gs_framework.quit()

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                gs_framework.quit()
            elif event.key == SDLK_UP:
                menu_index -= 1
                if menu_index < 0:
                    menu_index = 2
            elif event.key == SDLK_DOWN:
                menu_index += 1
                if menu_index > 2:
                    menu_index = 0
            elif event.key == SDLK_x:
                if menu_index == 0:
                    gs_framework.change_state(gs_stage_enter)
                elif menu_index == 1:
                    pass
                elif menu_index == 2:
                    gs_framework.quit()


def update():
    pass


def draw():
    global logo
    global menu
    global menu_outline
    global cursor_pos
    global cursor

    clear_canvas()

    logo.draw(gs_framework.canvas_width // 2, gs_framework.canvas_height // 2)

    if menu_index == 0:
        cursor_pos = [gs_framework.canvas_width // 2 - 200, gs_framework.canvas_height // 2 - 48]
    elif menu_index == 1:
        cursor_pos = [gs_framework.canvas_width // 2 - 200, gs_framework.canvas_height // 2 - 128]
    elif menu_index == 2:
        cursor_pos = [gs_framework.canvas_width // 2 - 200, gs_framework.canvas_height // 2 - 208]

    cursor.draw(cursor_pos[0], cursor_pos[1])

    menu[0].draw(gs_framework.canvas_width // 2 - 150,
                 gs_framework.canvas_height // 2 - 50,
                 "START GAME", (255, 255, 255))
    menu_outline[0].draw(gs_framework.canvas_width // 2 - 150,
                         gs_framework.canvas_height // 2 - 50,
                         "START GAME", (0, 0, 0))

    menu[1].draw(gs_framework.canvas_width // 2 - 150,
                 gs_framework.canvas_height // 2 - 130,
                 "EDIT STAGE", (255, 255, 255))
    menu_outline[1].draw(gs_framework.canvas_width // 2 - 150,
                         gs_framework.canvas_height // 2 - 130,
                         "EDIT STAGE", (0, 0, 0))

    menu[2].draw(gs_framework.canvas_width // 2 - 150,
                 gs_framework.canvas_height // 2 - 210,
                 "EXIT GAME", (255, 255, 255))
    menu_outline[2].draw(gs_framework.canvas_width // 2 - 150,
                         gs_framework.canvas_height // 2 - 210,
                         "EXIT GAME", (0, 0, 0))

    update_canvas()

    delay(0.05)



def pause():
    pass


def resume():
    pass


def test_gs_title():
    global logo
    global menu
    global cursor
    global menu_index
    global cursor_pos

    open_canvas(gs_framework.canvas_width, gs_framework.canvas_height)

    enter()

    loop = True

    while loop:
        clear_canvas()

        Events = get_events()

        for event in Events:
            if event.type == SDL_QUIT:
                loop = False

            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    loop = False
                elif event.key == SDLK_UP:
                    menu_index -= 1
                    if menu_index < 0:
                        menu_index = 2
                elif event.key == SDLK_DOWN:
                    menu_index += 1
                    if menu_index > 2:
                        menu_index = 0
                elif event.key == SDLK_x:
                    if menu_index == 0:
                        pass
                    elif menu_index == 1:
                        pass
                    elif menu_index == 2:
                        loop = False

        draw()
        update_canvas()

    close_canvas()

    return True


if __name__ == "__main__":
    print("== gs_title.py is prepared.")
    print("== start testing gs_title.py\n")
    if test_gs_title():
        print("\n== testing gs_title.py is done.")
    else:
        print("\n== error: testing gs_title.py is crashed")
