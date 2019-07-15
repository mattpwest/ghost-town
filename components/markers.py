"""
Marker components for entities that can and cannot move around the map.
"""


class Movable:
    def __init__(self):
        pass


class Creature(Movable):
    def __init__(self):
        Movable.__init__(self)


class Player(Movable):
    def __init__(self):
        Movable.__init__(self)


class Item(Movable):
    def __init__(self):
        Movable.__init__(self)


class Static:
    def __init__(self):
        pass


class Terrain(Static):
    def __init__(self):
        Static.__init__(self)
