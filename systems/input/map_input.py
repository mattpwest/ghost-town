import logging

import esper
import tcod.event
import tcod.event_constants as keys

from components import Player, Actor
from components.action import *


class MapInputSystem(esper.Processor):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

    def process(self):
        for entity, (actor, player) in self.world.get_components(Actor, Player):
            if actor.energy >= actor.cost:
                action = self.handle_input()
                self.world.add_component(entity, action)

    def handle_input(self):
        result = None

        while result is None:
            for event in tcod.event.wait():
                if event.type == 'QUIT':
                    result = QuitAction()
                elif event.type == 'KEYDOWN':
                    result = self.handle_keys(event)

        return result

    def handle_keys(self, event):
        if event.sym == keys.K_UP:
            return move(0, -1)
        elif event.sym == keys.K_DOWN:
            return move(0, 1)
        elif event.sym == keys.K_LEFT:
            return move(-1, 0)
        elif event.sym == keys.K_RIGHT:
            return move(1, 0)
        elif event.sym == keys.K_COMMA:
            return PickupAction()
        elif event.sym == keys.K_l:
            return LookAction()
        elif event.sym == keys.K_i:
            return OpenInventoryAction()
        elif event.sym == keys.K_PERIOD:
            return NoAction()
        elif event.sym == keys.K_RETURN and event.mod & tcod.event.KMOD_ALT:
            return FullscreenAction()
        elif event.sym == keys.K_ESCAPE:
            return MenuAction()

        self.log.warning("No configured key pressed.")
        return {}


def move(x, y):
    return MoveAction((x, y))
