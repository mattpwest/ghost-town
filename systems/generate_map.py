import logging

import esper

from states import State


class GenerateMapSystem(esper.Processor):
    def __init__(self, game_state, game_map, entity_factory):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state
        self.map = game_map
        self.factory = entity_factory

    def process(self):
        # TODO: Fancy multi-step dungeon generation
        # TODO: Render dungeon generator state

        self.log.info("Generating map...")
        self.map.generate_map()

        self.log.info("Placing player...")
        self.add_player()

        self.log.info("Going to MAP state...")
        self.game.new_state = State.MAP

    def add_player(self):
        x = self.map.rooms[0].center().x
        y = self.map.rooms[0].center().y
        player_entity = self.factory.player(x, y)
        self.map.entities[x][y] = player_entity
