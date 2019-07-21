import logging

import esper
import tcod.event
import tcod.event_constants as keys

from components import Player
from components.action import *


class DeadInputSystem(esper.Processor):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

    def process(self):
        for entity, player in self.world.get_component(Player):
            action = handle_input()
            self.log.debug("Dead player action: " + type(action).__name__)
            self.world.add_component(entity, action)


def handle_input():
    result = None

    while result is None:
        for event in tcod.event.wait():
            if event.type == 'QUIT':
                result = QuitAction()
            elif event.type == 'KEYDOWN':
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
    # elif event.sym == keys.K_COMMA:
    #     return PickupAction()
    # elif event.sym == keys.K_DECIMALSEPARATOR:
    #     return NoAction()
    if event.sym == keys.K_RETURN and event.mod & tcod.event.KMOD_ALT:
        return FullscreenAction()
    elif event.sym == keys.K_ESCAPE:
        return QuitAction()

    return NoAction()
