import logging

import esper

from components import Damage, Text, Player, Health, Position, Optics
from states import State


class DamageSystem(esper.Processor):
    def __init__(self, game):
        self.log = logging.getLogger("DamageSystem")
        self.log.setLevel(logging.WARN)

        self.game = game
        self.map = game.map
        self.messages = game.messages
        self.entity_factory = game.factory

    def process(self):
        for entity, (health, damage) in self.world.get_components(Health, Damage):
            self.log.debug("Applying " + str(damage.points) + " damage to " + str(entity))

            health.points -= damage.points
            self.world.remove_component(entity, Damage)

            if health.points <= 0:
                self.remove_from_map(entity)

                self.describe_death(entity)

                self.spawn_corpse(entity)

                self.world.delete_entity(entity)

    def spawn_corpse(self, entity):
        position = self.world.component_for_entity(entity, Position)
        text = self.world.component_for_entity(entity, Text)
        corpse = self.entity_factory.corpse(position.x, position.y, text.noun)
        self.map.items[position.x][position.y].append(corpse)

    def remove_from_map(self, entity):
        position = self.world.component_for_entity(entity, Position)
        self.map.entities[position.x][position.y] = None

    def describe_death(self, entity):
        if self.world.has_component(entity, Player):
            message = "You have died!"
            self.game.new_state = State.DEAD
        else:
            text = self.world.component_for_entity(entity, Text)
            message = "The " + text.noun + " dies!"

        self.log.info(message)
        self.messages.add(message)
