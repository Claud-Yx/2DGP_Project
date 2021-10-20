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


def show_keyboard(x = 50, y = 550):
    TK_BG.draw(x + 64 * 2, y - 32)
    TK_UP.clip_draw(64 * 0, 64 * TK_UP_KEY_STATE, 64, 64, x + 64 * 3, y)
    TK_DOWN.clip_draw(64 * 1, 64 * TK_DOWN_KEY_STATE, 64, 64, x + 64 * 3, y - 64)
    TK_LEFT.clip_draw( 64 * 2, 64 * TK_LEFT_KEY_STATE, 64, 64, x + 64 * 2, y - 64)
    TK_RIGHT.clip_draw(64 * 3, 64 * TK_RIGHT_KEY_STATE, 64, 64, x + 64 * 4, y - 64)
    TK_Z.clip_draw(64 * 4, 64 * TK_Z_KEY_STATE, 64, 64, x + 64 * 0, y - 64)
    TK_X.clip_draw(64 * 5, 64 * TK_X_KEY_STATE, 64, 64, x + 64 * 1, y - 64)


def keyboard_handle(g_events):

    # g_events = get_events()

    global SHOW_KEYBOARD
    global TK_UP_KEY_STATE, TK_DOWN_KEY_STATE, TK_LEFT_KEY_STATE,\
        TK_RIGHT_KEY_STATE, TK_Z_KEY_STATE, TK_X_KEY_STATE

    for event in g_events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_k:
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


def update_test_keyboard(x = 50, y = 550):
    global SHOW_KEYBOARD

    if SHOW_KEYBOARD:
        show_keyboard(x, y)


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

