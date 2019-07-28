import logging

import esper

from components import HealingEffect, Health


class EffectsSystem(esper.Processor):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

        self.log.debug("Initialized!")

    def process(self):
        for entity, (health, effect) in self.world.get_components(Health, HealingEffect):
            self.log.debug("HealingEffect on %s has %s time passed and %s duration remaining.",
                           entity, effect.time, effect.duration)

            if effect.time >= effect.interval:
                effect.time -= effect.interval
                effect.duration -= effect.interval

                health.points = min(health.points + effect.hit_points, health.maximum)

            if effect.duration <= 0:
                self.world.remove_component(entity, type(effect))
