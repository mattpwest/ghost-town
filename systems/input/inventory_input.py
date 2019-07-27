import logging

import esper
import tcod.event
import tcod.event_constants as keys

from states import State


class InventoryInputSystem(esper.Processor):
    def __init__(self, game_map, game_state):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.map = game_map
        self.game = game_state

    def process(self):
        action = handle_input()

        if action["quit"]:
            self.game.new_state = State.MAP


def handle_input():
    result = None

    while result is None:
        for event in tcod.event.wait():
            if event.type == 'KEYDOWN':
                result = handle_keys(event)

    return result


def handle_keys(event):
    # if event.sym == keys.K_UP:
    #     return move(0, -1)
    # elif event.sym == keys.K_DOWN:
    #     return move(0, 1)
    # elif event.sym == keys.K_LEFT:
    #     return move(-1, 0)
    # elif event.sym == keys.K_RIGHT:
    #     return move(1, 0)
    if event.sym == keys.K_ESCAPE:
        return {"delta": (0, 0), "quit": True}

    return {"delta": (0, 0), "quit": False}
