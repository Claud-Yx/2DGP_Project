from value import *

import server
import gs_framework
import game_object


class TileSet(game_object.Object):

    def __init__(self, tid=TID.NONE, x=0, y=0):
        super().__init__(TN.TILESETS, tid, x, y)

        self.set_info()

        # Object moving value
        del self.max_velocity
        del self.velocity
        # Animation Direction

        del self.facing
        del self.x_direction
        del self.y_direction

        # Object action with sprite animation
        del self.action

        # Animation frame value
        del self.time_per_action
        del self.action_per_time
        del self.frame
        del self.frame_begin
        del self.frame_count

        # Animation control value
        del self.loop_animation

    def update(self):
        if self.is_time_stop:
            return

        server.move_camera_x(self)
        # self.y -= server.player.jump_power * gs_framework.frame_time

    def draw(self):
        self.image_draw()

        if self.show_bb:
            self.draw_bb()

    def handle_event(self):
        pass


def test_tileset():
    import pico2d

    pico2d.open_canvas()
    Running = True
    show_bb = False

    tiles = [
        TileSet(TID.CASTLE_BLOCK_50X50, 200, 450),
        TileSet(TID.CASTLE_BLOCK_50X100, 600, 450),
        TileSet(TID.CASTLE_BLOCK_100X50, 200, 150),
        TileSet(TID.CASTLE_BLOCK_100X100, 600, 150),
        TileSet(x=400, y=300)
    ]

    for tile in tiles:
        print("tile bb: " + str(tile.bounding_box[HB.BODY].range))

    while Running:
        pico2d.clear_canvas()

        events = pico2d.get_events()
        for event in events:
            if event.type == pico2d.SDL_QUIT:
                Running = False
            elif (event.type, event.key) == (pico2d.SDL_KEYDOWN, pico2d.SDLK_ESCAPE):
                Running = False
            elif (event.type, event.key) == (pico2d.SDL_KEYDOWN, pico2d.SDLK_F2):
                print("in debugging")
                if not show_bb:
                    show_bb = True
                    for tile in tiles:
                        tile.show_bb = True
                else:
                    show_bb = False
                    for tile in tiles:
                        tile.show_bb = False

        for tile in tiles:
            try:
                tile.draw()
            except:
                print("Error - tile_name: " + tile.type_name + " tile_id: " + tile.type_id)
                exit(-1)

        pico2d.update_canvas()

    pico2d.close_canvas()


if __name__ == "__main__":
    test_tileset()