from pico2d import *

import gs_framework
import server


class Background:
    image = None

    def __init__(self, bwp=1.0, bhp=1.0, fwp=1.0, fhp=1.0):
        if Background.image is None:
            Background.image = {
                "back": load_image('resource\\background\\castle1_back.png'),
                "front": load_image('resource\\background\\castle1_front.png')
            }
        self.show_bb = True

        self.bwp, self.bhp = bwp, bhp
        self.fwp, self.fhp = fwp, fhp

        self.cw, self.ch = gs_framework.canvas_width, gs_framework.canvas_height
        self.bw, self.bh = Background.image["back"].w * self.bwp, Background.image["back"].h * self.bhp
        self.fw, self.fh = Background.image["front"].w * self.fwp, Background.image["front"].h * self.fhp

        self.bx, self.by = 0, 0
        self.fx, self.fy = 0, 0

        server.move_bg(self)

    def update(self):
        server.move_bg(self)

        # background[0] update
        while not 0 <= self.bx < self.bw:
            if self.bx < 0:
                self.bx += self.bw
            elif self.bx >= self.bw:
                self.bx -= self.bw

        while not 0 <= self.by < self.bh:
            if self.by < 0:
                self.by += self.bh
            elif self.by >= self.bh:
                self.by -= self.bh

        # background[1] update
        while not 0 <= self.fx < self.fw:
            if self.fx < 0:
                self.fx += self.fw
            elif self.fx >= self.fw:
                self.fx -= self.fw

        while not 0 <= self.fy < self.fh:
            if self.fy < 0:
                self.fy += self.fh
            elif self.fy >= self.fh:
                self.fy -= self.fh

    def draw_to_origin(self, x, y, layer):
        if Background.image is None:
            Background.image = {
                "back": load_image('resource\\background\\castle1_back.png'),
                "front": load_image('resource\\background\\castle1_front.png')
            }

        if layer == "back":
            Background.image[layer].draw_to_origin(x, y, self.bw, self.bh)
        else:
            Background.image[layer].draw_to_origin(x, y, self.fw, self.fh)

    def draw(self):
        self.draw_to_origin(self.bx, self.by, "back")
        if self.bx > 0:
            self.draw_to_origin(self.bx - self.bw, self.by, "back")
            if self.by > 0:
                self.draw_to_origin(self.bx - self.bw, self.by - self.bh, "back")
        if self.by > 0:
            self.draw_to_origin(self.bx, self.by - self.bh, "back")

        if self.bx + self.bw < self.cw:
            cw = int(self.cw // self.bw)
            for i in range(1, cw + 1):
                self.draw_to_origin(self.bx + self.bw * i, self.by, "back")
                if self.by > 0:
                    self.draw_to_origin(self.bx + self.bw * i, self.by - self.bh, "back")
            if self.by + self.bh < self.ch:
                ch = int(self.ch // self.bh)
                for i in range(1, cw + 1):
                    for j in range(1, ch + 1):
                        self.draw_to_origin(self.bx + self.bw * i, self.by + self.bh * j, "back")

        if self.by + self.bh < self.ch:
            ch = int(self.ch // self.bh)
            for i in range(1, ch + 1):
                self.draw_to_origin(self.bx, self.by + self.bh * i, "back")
                if self.bx > 0:
                    self.draw_to_origin(self.bx - self.bw, self.by + self.bh * i, "back")

        self.draw_to_origin(self.fx, self.fy, "front")
        if self.fx > 0:
            self.draw_to_origin(self.fx - self.fw, self.fy, "front")
            if self.fy > 0:
                self.draw_to_origin(self.fx - self.fw, self.fy - self.fh, "front")
        if self.fy > 0:
            self.draw_to_origin(self.fx, self.fy - self.fh, "front")

        if self.fx + self.fw < self.cw:
            cw = int(self.cw // self.fw)
            for i in range(1, cw + 1):
                self.draw_to_origin(self.fx + self.fw * i, self.fy, "front")
                if self.fy > 0:
                    self.draw_to_origin(self.fx + self.fw * i, self.fy - self.fh, "front")
            if self.fy + self.fh < self.ch:
                ch = int(self.ch // self.fh)
                for i in range(1, cw + 1):
                    for j in range(1, ch + 1):
                        self.draw_to_origin(self.fx + self.fw * i, self.fy + self.fh * j, "front")

        if self.fy + self.fh < self.ch:
            ch = int(self.ch // self.fh)
            for i in range(1, ch + 1):
                self.draw_to_origin(self.fx, self.fy + self.fh * i, "front")
                if self.fx > 0:
                    self.draw_to_origin(self.fx - self.fw, self.fy + self.fh * i, "front")

    def handle_event(self):
        pass
