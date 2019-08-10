import logging
import random
from random import Random
import sys

from components import Tangible


class GameMap:
    def __init__(self, config, world, entity_factory):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.config = config.map

        self.world = world
        self.factory = entity_factory

        self.tiles = self.initialize_tiles()
        self.items = self.initialize_items()
        self.entities = self.initialize_entities()
        self.rooms = []

        self.seed = random.randint(0, sys.maxsize)
        self.rng = Random(self.seed)

    def clear(self):
        self.world.clear_database()

        self.tiles = self.initialize_tiles()
        self.items = self.initialize_items()
        self.entities = self.initialize_entities()
        self.rooms = []

        self.seed = random.randint(0, sys.maxsize)
        self.rng = Random(self.seed)

    def initialize_tiles(self):
        return [[self.factory.wall(x, y) for y in range(self.config.height)] for x in range(self.config.width)]

    def initialize_items(self):
        return [[[] for y in range(self.config.height)] for x in range(self.config.width)]

    def initialize_entities(self):
        return [[None for y in range(self.config.height)] for x in range(self.config.width)]

    def generate_map(self):
        self.log.debug("Generating map with " +
                       "{width=" + str(self.config.width) +
                       "; height=" + str(self.config.height) +
                       "; max_rooms=" + str(self.config.max_rooms) +
                       "; room_max_size=" + str(self.config.room_max_size) +
                       "; room_min_size=" + str(self.config.room_min_size) +
                       "}"
                       )
        for room_number in range(self.config.max_rooms):
            w = self.rng.randint(self.config.room_min_size, self.config.room_max_size)
            h = self.rng.randint(self.config.room_min_size, self.config.room_max_size)

            x = self.rng.randint(0, self.config.width - w - 1)
            y = self.rng.randint(0, self.config.height - h - 1)

            new_room = Rect(x, y, w, h)

            if self.intersects_existing_room(new_room, self.rooms):
                continue

            self.create_room(new_room)

            if len(self.rooms) != 0:
                self.connect_rooms(new_room, self.rooms[len(self.rooms) - 1])

            if room_number != 0:
                self.place_entities(new_room, self.config.room_max_monsters)

            self.place_items(new_room, self.config.room_max_items)

            self.rooms.append(new_room)

    def intersects_existing_room(self, new_room, rooms):
        for other_room in rooms:
            if new_room.intersect(other_room):
                return True

        return False

    def connect_rooms(self, room1, room2):
        center1 = room1.center()
        center2 = room2.center()

        if self.rng.randint(0, 1) == 1:
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
        number_of_monsters = self.rng.randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            x = self.rng.randint(room.x1 + 1, room.x2 - 1)
            y = self.rng.randint(room.y1 + 1, room.y2 - 1)
            logging.debug("Monster " + str(i) + " at (" + str(x) + ", " + str(y) + ")")

            if self.entities[x][y] is None:
                if self.rng.randint(0, 100) < 80:
                    monster = self.factory.orc(x, y)
                else:
                    monster = self.factory.troll(x, y)

                self.entities[x][y] = monster

    def place_items(self, room, room_max_items):
        logging.debug("Placing monsters...")

        number = self.rng.randint(0, room_max_items)
        for i in range(number):
            x = self.rng.randint(room.x1 + 1, room.x2 - 1)
            y = self.rng.randint(room.y1 + 1, room.y2 - 1)

            self.items[x][y].append(self.factory.potion_healing(x, y))


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
