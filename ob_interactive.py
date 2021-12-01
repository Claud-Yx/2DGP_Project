from abc import ABC

from game_object import *


class WireMesh(GameObject, ABC):
    def __init__(self, x, y):
        super().__init__(TN.INTERACTIVES, TID.WIRE_MESH, x, y)

        