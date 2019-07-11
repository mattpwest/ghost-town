import logging

import esper

from components import Damage, Text, Player, Health, Position


class DamageSystem(esper.Processor):
    def __init__(self, game_map):
        self.log = logging.getLogger("DamageSystem")
        self.log.setLevel(logging.INFO)

        self.map = game_map

    def process(self):
        for entity, (health, damage) in self.world.get_components(Health, Damage):
            self.log.debug("Applying " + str(damage.points) + " damage to " + str(entity))
            health.points -= damage.points

            if health.points <= 0:
                self.remove_from_map(entity)
                # TODO: Figure out how to update vision map as well

                self.describe_death(entity)

                self.world.delete_entity(entity)

    def remove_from_map(self, entity):
        position = self.world.component_for_entity(entity, Position)
        self.map.entities[position.x][position.y] = None

    def describe_death(self, entity):
        if self.world.has_component(entity, Player):
            self.log.info("You have died!")
        else:
            text = self.world.component_for_entity(entity, Text)
            self.log.info("The " + text.noun + " dies!")
