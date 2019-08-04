import logging

import esper
import tcod as libtcod

from components import Damage, Text, Health, Position, Essence, Possessor, EssenceAbsorber


class DamageSystem(esper.Processor):
    def __init__(self, game_state, game_map, message_log, entity_factory, config):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state
        self.map = game_map
        self.messages = message_log
        self.entity_factory = entity_factory
        self.config = config

    def process(self):
        for entity, (health, damage) in self.world.get_components(Health, Damage):
            self.log.debug("Applying " + str(damage.points) + " damage to " + str(entity))

            health.points -= damage.points
            self.log.debug(str(entity) + " has " + str(health.points) + " HP")
            self.world.remove_component(entity, Damage)

            if health.points <= 0:
                self.remove_from_map(entity)

                self.describe_death(entity)

                if self.world.has_component(entity, Possessor):
                    self.exorcise(entity)
                else:
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
        if self.world.has_component(entity, Possessor):
            text = self.world.component_for_entity(entity, Text)
            color = self.config.colors.message_warning
            message = "The " + text.noun + " has died! Your spirit survives..."
        else:
            color = libtcod.white
            text = self.world.component_for_entity(entity, Text)
            message = "The " + text.noun + " dies!"

        self.log.info(message)
        self.messages.add(message, color)

    def drop_essence(self, entity):
        if not self.world.has_component(entity, Essence) or not self.world.has_component(entity, Position):
            return

        essence = self.world.component_for_entity(entity, Essence)
        position = self.world.component_for_entity(entity, Position)

        tile_essence = self.world.component_for_entity(self.map.tiles[position.x][position.y], Essence)
        tile_essence.value += essence.value

    def delete_entity(self, entity):
        self.world.delete_entity(entity)

    def exorcise(self, entity):
        position = self.world.component_for_entity(entity, Position)
        possessor = self.world.component_for_entity(entity, Possessor)
        essence = self.world.component_for_entity(entity, Essence)
        absorber = self.world.component_for_entity(entity, EssenceAbsorber)

        player = self.world.create_entity()
        self.world.add_component(player, essence)
        self.world.add_component(player, absorber)
        for component in possessor.my_components:
            self.world.add_component(player, component)

            if isinstance(component, Position):
                component.x = position.x
                component.y = position.y
                self.map.entities[position.x][position.y] = player
