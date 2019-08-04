import copy
import logging

import esper

from components import Text, Player, Possession, Essence, Possessor, Creature, Render, EssenceAbsorber, Optics, \
    Position, EssenceDrain


class PossessionSystem(esper.Processor):
    def __init__(self, game_map, message_log):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.WARN)

        self.map = game_map
        self.messages = message_log

    def process(self):
        for target, (possession, target_essence, text)\
                in self.world.get_components(Possession, Essence, Text):
            possessor = self.world.component_for_entity(possession.from_entity, Possessor)
            possessor_essence = self.world.component_for_entity(possession.from_entity, Essence)
            possessor_absorber = self.world.component_for_entity(possession.from_entity, EssenceAbsorber)
            possessor_drain = self.world.component_for_entity(possession.from_entity, EssenceDrain)
            possessor_position = self.world.component_for_entity(possession.from_entity, Position)

            cost = target_essence.value * possessor.cost_multiplier
            if cost > possessor_essence.value:
                self.messages.add("Your essence is not strong enough to overcome the " + text.noun + ".")
                continue

            possessor_essence.value -= cost

            for component in self.world.components_for_entity(possession.from_entity):
                if component != possessor_essence and component != possessor_absorber:
                    possessor.my_components.append(copy.deepcopy(component))

            target_creature = self.world.component_for_entity(target, Creature)
            target_render = self.world.component_for_entity(target, Render)
            possessor.target_components.append(copy.deepcopy(target_creature))
            possessor.target_components.append(copy.deepcopy(target_render))
            possessor.target_components.append(copy.deepcopy(target_essence))

            self.world.remove_component(target, Creature)
            self.world.remove_component(target, Essence)
            self.world.remove_component(target, Possession)
            target_render.char = "@"

            self.world.add_component(target, Player())
            self.world.add_component(target, copy.deepcopy(possessor))
            self.world.add_component(target, copy.deepcopy(possessor_essence))
            self.world.add_component(target, copy.deepcopy(possessor_absorber))
            drain = copy.deepcopy(possessor_drain)
            drain.value = drain.value * possessor.cost_multiplier
            self.world.add_component(target, copy.deepcopy(possessor_drain))
            self.world.component_for_entity(target, Optics).transparent = False

            self.world.delete_entity(possession.from_entity)
            self.map.entities[possessor_position.x][possessor_position.y] = None

            self.messages.add("You take control of the " + text.noun + "'s body!")
