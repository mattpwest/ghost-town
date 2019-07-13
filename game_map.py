import logging
from random import randint

from components import Tangible


class GameMap:
    def __init__(self, width, height, world, factory):
        self.width = width
        self.height = height
        self.world = world
        self.factory = factory

        self.tiles = self.initialize_tiles()
        self.entities = self.initialize_entities()
        self.rooms = []

    def initialize_tiles(self):
        return [[self.factory.wall(x, y) for y in range(self.height)] for x in range(self.width)]

    def initialize_entities(self):
        return [[None for y in range(self.height)] for x in range(self.width)]

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, max_monsters_per_room):
        for room_number in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            if self.intersects_existing_room(new_room, self.rooms):
                continue

            self.create_room(new_room)

            if len(self.rooms) != 0:
                self.connect_rooms(new_room, self.rooms[len(self.rooms) - 1])

            self.place_entities(new_room, max_monsters_per_room)

            self.rooms.append(new_room)
    
    def intersects_existing_room(self, new_room, rooms):
        for other_room in rooms:
            if new_room.intersect(other_room):
                return True
        
        return False

    def connect_rooms(self, room1, room2):
        center1 = room1.center()
        center2 = room2.center()

        if randint(0, 1) == 1:
            self.create_h_tunnel(center2.x, center1.x, center2.y)
            self.create_v_tunnel(center2.y, center1.y, center1.x)
        else:
            self.create_v_tunnel(center2.y, center1.y, center2.x)
            self.create_h_tunnel(center2.x, center1.x, center1.y)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.dig(x, y)

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.dig(x, y)

    def is_blocked(self, x, y):
        return self.world.component_for_entity(self.tiles[x][y], Tangible).blocks_physical

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.dig(x, y)
    
    def dig(self, x, y):
        self.world.delete_entity(self.tiles[x][y])
        self.tiles[x][y] = self.factory.floor(x, y)
    
    def place_entities(self, room, max_monsters_per_room):
        logging.debug("Placing monsters...")
        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            logging.debug("Monster " + str(i) + " at (" + str(x) + ", " + str(y) + ")")

            if self.entities[x][y] is None:
                if randint(0, 100) < 80:
                    monster = self.factory.orc(x, y)
                else:
                    monster = self.factory.troll(x, y)

                self.entities[x][y] = monster


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return Point(center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y