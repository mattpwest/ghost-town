import logging
import sys

import esper

from components.actor import Actor

"""
ActionSystem uses Actor components to track energy on all entities that can act. Once an entity has enough energy to act
the system waits for that entity to finish acting, otherwise we find the next entity that can act and repeat.

If there are no entities that can act we tick the entities adding energy until someone can act again.
"""


class ActionSystem(esper.Processor):
    def __init__(self, game_state, game_map):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state
        self.map = game_map
        self.active = None

        self.log.debug("Initialized!")

    def process(self):
        for entity, actor in self.world.get_component(Actor):
            if not self.can_act(actor):
                self.tick(entity, actor)
            else:
                self.log.debug(str(entity) + " is ready to act.")

    def tick(self, entity, actor):
        actor.energy += actor.gain
        self.log.debug('Tick %s, energy=%s', entity, actor.energy)

    def can_act(self, actor):
        return actor.energy >= actor.cost
