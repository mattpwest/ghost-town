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
    def __init__(self, game):
        self.log = logging.getLogger("ActionSystem")
        self.log.setLevel(logging.INFO)
        self.log.debug("ActionSystem initialized!")

        self.game = game
        self.active = None

    def process(self):
        # Short-circuit this system to make quit trigger immediately
        if not self.game.running:
            return

        for entity, actor in self.world.get_component(Actor):
            if self.can_act(actor):
                action = actor.strategy.act(entity, self.world, self.game.map)
                self.world.add_component(entity, action)
            else:
                self.tick(entity, actor)

    def tick(self, entity, actor):
        actor.energy += actor.gain
        self.log.debug('Tick %s, energy=%s', entity, actor.energy)

    def can_act(self, actor):
        return actor.energy >= actor.cost
