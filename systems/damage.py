import copy
import logging

import esper

from components import Damage, Text, Player, Health, Position, Tangible, Render, Essence, Terrain
from states import State


class DamageSystem(esper.Processor):
    def __init__(self, game_state, game_map, message_log, entity_factory):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state
        self.map = game_map
        self.messages = message_log
        self.entity_factory = entity_factory

    def process(self):
        for entity, (health, damage) in self.world.get_components(Health, Damage):
            self.log.debug("Applying " + str(damage.points) + " damage to " + str(entity))

            health.points -= damage.points
            self.log.debug(str(entity) + " has " + str(health.points) + " HP")
            self.world.remove_component(entity, Damage)

            if health.points <= 0:
                self.remove_from_map(entity)

                self.describe_death(entity)

                self.drop_essence(entity)

                self.spawn_corpse(entity)

                self.delete_entity(entity)

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

    def drop_essence(self, entity):
        if not self.world.has_component(entity, Essence) or not self.world.has_component(entity, Position):
            return

        essence = copy.deepcopy(self.world.component_for_entity(entity, Essence))
        position = copy.deepcopy(self.world.component_for_entity(entity, Position))

        self.world.create_entity(essence, position, Terrain())

    def delete_entity(self, entity):
        if self.world.has_component(entity, Player):
            self.world.remove_component(entity, Tangible)
            self.world.remove_component(entity, Render)
        else:
            self.world.delete_entity(entity)
