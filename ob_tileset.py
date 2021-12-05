import ob_foreground
import ob_item
import object_manager
from value import *

import server
import gs_framework
import game_object

import pico2d

MAX_HIT_TIMER = 0.2
VELOCITY_HIT = get_pps_from_mps(10)


class RS(IntEnum):  # Random box state
    NORMAL = 0
    POLYMORPH = 1
    INVISIBLE = 2


class TileSet(game_object.GameObject):

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


class RandomBox(TileSet):
    def __init__(self, x=0, y=0, item=TID.COIN, state=RS.NORMAL):

        super().__init__(TID.RANDOM_BOX, x, y)

        self.min_y, self.max_y = y, y+20

        self.x_direction = DIR.RIGHT
        self.state = state

        self.action = ACTION.IDLE

        self.item = item

        self.is_empty = False
        self.is_hit = False

        self.timer_hit = 0.0

        if self.item == TID.NONE:
            self.is_empty = True
            self.is_hit = True

        # Animation frame value
        self.time_per_action = 0.0
        self.action_per_time = 0.0
        self.frame = 0
        self.frame_begin = 0
        self.frame_count = 0

        # Animation control value
        self.loop_animation = False
        self.set_info()

    def hit(self):
        if self.is_hit and not self.is_empty:
            if server.player.x > self.x:
                self.x_direction = DIR.LEFT

            if self.timer_hit == 0:
                if self.item == TID.COIN:
                    server.player.coin += 1
                    server.items.append(ob_item.Coin(self.x, self.y + self.h, True))
                    object_manager.add_object(server.items[-1], L.FOREGROUND)

                self.type_id = TID.EMPTY_BOX
                self.set_info()
                self.timer_hit = MAX_HIT_TIMER

            self.timer_hit -= gs_framework.frame_time

            if self.timer_hit >= MAX_HIT_TIMER / 2:
                self.y += VELOCITY_HIT * gs_framework.frame_time
            else:
                self.y -= VELOCITY_HIT * gs_framework.frame_time
            self.y = pico2d.clamp(self.min_y, self.y, self.max_y)

            if self.timer_hit <= 0.0:
                if self.item == TID.SUPER_MUSHROOM:
                    server.items.append(
                        ob_item.PowerUp(TID.SUPER_MUSHROOM,self.x, self.y, self.x_direction, True)
                    )
                    object_manager.add_object(server.items[-1], L.ITEMS)
                elif self.item == TID.LIFE_MUSHROOM:
                    server.items.append((
                        ob_item.PowerUp(TID.LIFE_MUSHROOM, self.x, self.y, self.x_direction, True)
                    ))
                    object_manager.add_object(server.items[-1], L.ITEMS)

                self.is_empty = True
                server.tiles.append(TileSet(TID.EMPTY_BOX, self.x, self.y))
                object_manager.add_object(server.tiles[-1], L.TILESETS)

    def empty(self):
        if self.is_hit and self.is_empty:
            object_manager.remove_object(self)
            del self
        else:
            self.update_frame(gs_framework.frame_time)

    def update(self):
        if self.is_time_stop:
            return

        server.move_camera_x(self)

        self.hit()
        self.empty()

    def draw(self):
        if self.type_id == TID.EMPTY_BOX:
            self.image_draw()
        elif self.state == RS.INVISIBLE:
            pass
        elif self.state == RS.POLYMORPH:
            self.clip_draw(TN.TILESETS, TID.BREAKABLE_BRICK)
        else:
            self.clip_draw()

        if self.show_bb:
            self.draw_bb()

        # self.y -= server.player.jump_power * gs_framework.frame_time


class Brick(TileSet):
    def __init__(self, x, y):
        super().__init__(TID.BREAKABLE_BRICK, x, y)

        self.min_y, self.max_y = y, y+20

        self.x_direction = DIR.RIGHT

        self.hit_by = None
        self.timer_hit = 0

        self.action = ACTION.IDLE

        # Animation frame value
        self.time_per_action = 0.0
        self.action_per_time = 0.0
        self.frame = 0
        self.frame_begin = 0
        self.frame_count = 0

        # Animation control value
        self.loop_animation = False
        self.set_info()

    def hit(self):
        if server.player.x > self.x:
            self.x_direction = DIR.LEFT

        if self.hit_by == TID.MARIO_SMALL:
            if self.timer_hit == 0:
                self.timer_hit = MAX_HIT_TIMER

            self.timer_hit -= gs_framework.frame_time

            if self.timer_hit >= MAX_HIT_TIMER / 2:
                self.y += VELOCITY_HIT * gs_framework.frame_time
            else:
                self.y -= VELOCITY_HIT * gs_framework.frame_time
            self.y = pico2d.clamp(self.min_y, self.y, self.max_y)

            if self.timer_hit <= 0.0:
                self.hit_by = None
                self.timer_hit = 0

        elif self.hit_by is not None:
            server.foreground.append(ob_foreground.BrickPiece(
                self.x - self.w * (1/4), self.y + self.h * (1/4), ACTION.PIECE_LT))
            object_manager.add_object(server.foreground[-1], L.FOREGROUND)
            server.foreground.append(ob_foreground.BrickPiece(
                self.x - self.w * (1/4), self.y - self.h * (1/4), ACTION.PIECE_LB))
            object_manager.add_object(server.foreground[-1], L.FOREGROUND)
            server.foreground.append(ob_foreground.BrickPiece(
                self.x + self.w * (1/4), self.y - self.h * (1/4), ACTION.PIECE_RT))
            object_manager.add_object(server.foreground[-1], L.FOREGROUND)
            server.foreground.append(ob_foreground.BrickPiece(
                self.x + self.w * (1/4), self.y + self.h * (1/4), ACTION.PIECE_RB))
            object_manager.add_object(server.foreground[-1], L.FOREGROUND)

            object_manager.remove_object(self)
            del self
            return

    def update(self):
        if self.is_time_stop:
            return

        server.move_camera_x(self)
        self.update_frame(gs_framework.frame_time)

        self.hit()

    def draw(self):

        self.clip_draw()

        if self.show_bb:
            self.draw_bb()


class Spike(TileSet):
    def __init__(self, x, y, pos=POS.TOP):
        super().__init__(TID.SPIKE, x, y)

        self.action = ACTION.IDLE

        # Animation frame value
        self.frame = 0
        self.frame_begin = pos
        self.frame_count = 0

        # Animation control value
        self.loop_animation = False
        self.set_info()

    # def update(self):
    #     pass

    def draw(self):
        self.clip_draw()

        if self.show_bb:
            self.draw_bb()

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