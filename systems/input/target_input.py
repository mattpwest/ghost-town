import logging

import esper
import tcod.event
import tcod.event_constants as keys

from components import Target, Position, Optics
from states import State


class TargetInputSystem(esper.Processor):
    def __init__(self, game_map, game_state):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.map = game_map
        self.game = game_state

    def process(self):
        for entity, (position, target) in self.world.get_components(Position, Target):
            action = handle_input()

            if action["quit"]:
                self.game.new_state = State.MAP
                self.world.delete_entity(entity)
                return

            tx = position.x + action["delta"][0]
            ty = position.y + action["delta"][1]

            tile = self.map.tiles[tx][ty]
            optics = self.world.component_for_entity(tile, Optics)
            if optics and optics.lit:
                position.x = tx
                position.y = ty


def handle_input():
    result = None

    while result is None:
        for event in tcod.event.wait():
            if event.type == 'KEYDOWN':
                result = handle_keys(event)

    return result


def handle_keys(event):
    if event.sym == keys.K_UP:
        return move(0, -1)
    elif event.sym == keys.K_DOWN:
        return move(0, 1)
    elif event.sym == keys.K_LEFT:
        return move(-1, 0)
    elif event.sym == keys.K_RIGHT:
        return move(1, 0)
    elif event.sym == keys.K_ESCAPE:
        return {"delta": (0, 0), "quit": True}

    return {"delta": (0, 0), "quit": False}


def move(x, y):
    return {"delta": (x, y), "quit": False}
