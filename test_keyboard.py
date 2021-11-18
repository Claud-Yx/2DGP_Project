from pico2d import *

TK_UP = None
TK_DOWN = None
TK_LEFT = None
TK_RIGHT = None
TK_Z = None
TK_X = None
TK_BG = None

TK_UP_KEY_STATE = 1 # 1 = up / 0 = press
TK_DOWN_KEY_STATE = 1
TK_LEFT_KEY_STATE = 1
TK_RIGHT_KEY_STATE = 1
TK_Z_KEY_STATE = 1
TK_X_KEY_STATE = 1
SHOW_KEYBOARD = False


def keyboard_init():
    global TK_UP, TK_DOWN, TK_LEFT, TK_RIGHT, TK_Z, TK_X, TK_BG

    TK_UP = load_image( 'resource\\keyboard.png' )
    TK_DOWN = load_image( 'resource\\keyboard.png' )
    TK_LEFT = load_image( 'resource\\keyboard.png' )
    TK_RIGHT = load_image( 'resource\\keyboard.png' )
    TK_Z = load_image( 'resource\\keyboard.png' )
    TK_X = load_image( 'resource\\keyboard.png' )
    TK_BG = load_image('resource\\keyboard_bg.png')

# standard location: left top
def show_keyboard(x = 50, y = 550, w = 1, h = 1):
    button_w = 64 * w
    button_h = 64 * h
    bg_w = 340 * w
    bg_h = 148 * h
    button_xi = 64 * w
    button_yi = 64 * h
    bg_xi = button_xi * 2
    bg_yi = button_yi / 2

    TK_BG.draw(x + bg_xi, y - bg_yi,
               bg_w, bg_h)

    TK_UP.clip_draw(64 * 0, 64 * TK_UP_KEY_STATE, 64, 64,
                    x + button_xi * 3, y, button_w, button_h)
    TK_DOWN.clip_draw(64 * 1, 64 * TK_DOWN_KEY_STATE, 64, 64,
                      x + button_xi * 3, y - button_yi, button_w, button_h)
    TK_LEFT.clip_draw( 64 * 2, 64 * TK_LEFT_KEY_STATE, 64, 64,
                       x + button_xi * 2, y - button_yi, button_w, button_h)
    TK_RIGHT.clip_draw(64 * 3, 64 * TK_RIGHT_KEY_STATE, 64, 64,
                       x + button_xi * 4, y - button_yi, button_w, button_h)
    TK_Z.clip_draw(64 * 4, 64 * TK_Z_KEY_STATE, 64, 64,
                   x + button_xi * 0, y - button_yi, button_w, button_h)
    TK_X.clip_draw(64 * 5, 64 * TK_X_KEY_STATE, 64, 64,
                   x + button_xi * 1, y - button_yi, button_w, button_h)


def keyboard_handle(g_events):

    # g_events = get_events()

    global SHOW_KEYBOARD
    global TK_UP_KEY_STATE, TK_DOWN_KEY_STATE, TK_LEFT_KEY_STATE,\
        TK_RIGHT_KEY_STATE, TK_Z_KEY_STATE, TK_X_KEY_STATE

    for event in g_events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_F4:
                if SHOW_KEYBOARD:
                    SHOW_KEYBOARD = False
                else:
                    SHOW_KEYBOARD = True

            elif event.key == SDLK_UP:
                TK_UP_KEY_STATE = 0
            elif event.key == SDLK_DOWN:
                TK_DOWN_KEY_STATE = 0
            elif event.key == SDLK_LEFT:
                TK_LEFT_KEY_STATE = 0
            elif event.key == SDLK_RIGHT:
                TK_RIGHT_KEY_STATE = 0
            elif event.key == SDLK_z:
                TK_Z_KEY_STATE = 0
            elif event.key == SDLK_x:
                TK_X_KEY_STATE = 0
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                TK_UP_KEY_STATE = 1
            elif event.key == SDLK_DOWN:
                TK_DOWN_KEY_STATE = 1
            elif event.key == SDLK_LEFT:
                TK_LEFT_KEY_STATE = 1
            elif event.key == SDLK_RIGHT:
                TK_RIGHT_KEY_STATE = 1
            elif event.key == SDLK_z:
                TK_Z_KEY_STATE = 1
            elif event.key == SDLK_x:
                TK_X_KEY_STATE = 1


def update_test_keyboard(x = 50, y = 550, w = 1, h = 1):
    global SHOW_KEYBOARD

    if SHOW_KEYBOARD:
        show_keyboard(x, y, w, h)


# open_canvas()
#
# keyboard_init()
#
# while True:
#     clear_canvas()
#
#     update_test_keyboard()
#
#     update_canvas()
#
#     delay(0.05)

