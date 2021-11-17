from value import *


class BoundingBox:
    def __init__(self, bid, ran):

        # Box info
        self.id = bid
        self.range = [ran[POS.LEFT], ran[POS.BOTTOM], ran[POS.RIGHT], ran[POS.TOP]]
        # self.prev_range = self.range

    def get_bb(self, pos):
        return (
            pos[POS.X] - self.range[POS.LEFT],
            pos[POS.Y] - self.range[POS.BOTTOM],
            pos[POS.X] + self.range[POS.RIGHT],
            pos[POS.Y] + self.range[POS.TOP]
        )

    def set_bb(self, ran):
        self.range = [ran[POS.LEFT], ran[POS.BOTTOM], ran[POS.RIGHT], ran[POS.TOP]]

