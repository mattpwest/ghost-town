import logging
import shelve
from copy import deepcopy

import esper

from states import State, Inventory


class SaveSystem(esper.Processor):
    def __init__(self, config, game_state, game_map):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

        self.config = config
        self.game = game_state
        self.map = game_map

    def process(self):
        save_tiles = []
        save_entities = []
        save_items = []
        for y in range(self.config.map.height):
            for x in range(self.config.map.width):
                tile = self.map.tiles[x][y]
                if tile:
                    save_tiles.append(self.get_components(tile))

                entity = self.map.entities[x][y]
                if entity:
                    save_entities.append(self.get_components(entity))

                items = self.map.items[x][y]
                for item in items:
                    save_items.append(self.get_components(item))

        self.log.debug("Saving %s tiles...", str(len(save_tiles)))
        self.log.debug("Saving %s entities...", str(len(save_entities)))
        self.log.debug("Saving %s items...", str(len(save_items)))
        self.log.warning("Not dealing with inventories - they will likely break!")

        save_entities.extend(save_tiles)
        save_entities.extend(save_items)
        with shelve.open("data/saves/game01", "n") as data_file:
            data_file["components"] = save_entities

        self.game.new_state = State.MAP

    def get_components(self, entity):
        result = []
        for component in self.world.components_for_entity(entity):
            if isinstance(component, Inventory):
                copy = self.copy_inventory_and_nest_items(component)
                result.append(copy)
            else:
                result.append(component)

        return result

    def copy_inventory_and_nest_items(self, component):
        items = []
        for item in component.items:
            items.append(self.get_components(item))
        component.items = items
        copy = deepcopy(component)
        copy.items = items
        return copy
