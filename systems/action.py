import logging

import esper

from components import HealingEffect
from components.actor import Actor

"""
ActionSystem uses Actor components to track energy on all entities that can act. Once an entity has enough energy to act
the system waits for that entity to finish acting, otherwise we find the next entity that can act and repeat.

If there are no entities that can act we tick the entities adding energy until someone can act again.
"""
# TODO: Considering renaming this the TimeSystem (or TimeWimeySystem if so inclined)


class ActionSystem(esper.Processor):
    def __init__(self, game_state, game_map):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state
        self.map = game_map
        self.active = None

        self.log.debug("Initialized!")

        self.time = 0

    def process(self):
        delta_time = 0
        cannot_act = []
        for entity, actor in self.world.get_component(Actor):
            if not self.can_act(actor):
                cannot_act.append((entity, actor))
            else:
                self.log.debug(str(entity) + " is ready to act.")
                return

        for inactive in cannot_act:
            entity = inactive[0]
            actor = inactive[1]

            actor.energy += actor.gain
            self.log.debug("Ticked %s, energy=%s", entity, actor.energy)

            delta_time = max(delta_time, actor.gain)

        if delta_time != 0:
            self.time += delta_time
            self.log.info("%s time has passed...", str(self.time))

            # TODO: Bit crap - seems we have to do this per effect...
            for entity, (actor, effect) in self.world.get_components(Actor, HealingEffect):
                self.log.info("Allocating %s time to effect %s for entity %s",
                              str(delta_time), str(effect), str(entity))
                effect.time += delta_time

    def can_act(self, actor):
        return actor.energy >= actor.cost
