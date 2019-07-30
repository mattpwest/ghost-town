import logging
import os
import shelve

import esper

from components import Position, Terrain, Creature, Player, Item
from states import State


class LoadSystem(esper.Processor):
    def __init__(self, game_state, game_map):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state
        self.map = game_map

    def process(self):
        self.map.clear()

        filename = "data/saves/game01"

        if not os.path.isfile(filename + ".dat"):
            raise FileNotFoundError

        with shelve.open(filename, "r") as data_file:
            for components in data_file["components"]:
                entity = self.world.create_entity()

                for component in components:
                    self.world.add_component(entity, component)

        for entity, (position, terrain) in self.world.get_components(Position, Terrain):
            self.map.tiles[position.x][position.y] = entity

        for entity, (position, creature) in self.world.get_components(Position, Creature):
            self.map.entities[position.x][position.y] = entity

        for entity, (position, player) in self.world.get_components(Position, Player):
            self.map.entities[position.x][position.y] = entity

        for entity, (position, item) in self.world.get_components(Position, Item):
            self.map.items[position.x][position.y].append(entity)

        self.game.new_state = State.MAP
