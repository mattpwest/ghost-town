import copy
import logging

import esper

from components import Inventory, Item, Text, DropAction, DrinkAction, Effect, ThrowAction
from components.actor import Actor
from components.position import Position


class InventoryActionsSystem(esper.Processor):
    def __init__(self, game_map, message_log):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.map = game_map
        self.messages = message_log

    def process(self):
        for entity, (actor, position, inventory, action) \
                in self.world.get_components(Actor, Position, Inventory, DropAction):
            inventory.items.remove(action.item)
            self.map.items[position.x][position.y].append(action.item)

            self.world.add_component(action.item, Item())  # Enable rendering on map

            item_position = self.world.component_for_entity(action.item, Position)
            item_position.x = position.x
            item_position.y = position.y

            item_text = self.world.component_for_entity(action.item, Text)
            self.messages.add("You drop the " + item_text.noun + " on the floor.")

            actor.energy -= action.cost
            self.world.remove_component(entity, DropAction)

        for entity, (actor, inventory, action) in self.world.get_components(Actor, Inventory, DrinkAction):
            for component in self.world.components_for_entity(action.item):
                if isinstance(component, Effect):
                    self.world.add_component(entity, copy.copy(component))

                if isinstance(component, Text):
                    self.messages.add("You drink a " + component.noun + ".")

            inventory.items.remove(action.item)
            self.world.delete_entity(action.item)

            actor.energy -= action.cost
            self.world.remove_component(entity, DrinkAction)

        for entity, (actor, inventory, action) in self.world.get_components(Actor, Inventory, ThrowAction):
            target_text = self.world.component_for_entity(action.target, Text)

            for component in self.world.components_for_entity(action.item):
                if isinstance(component, Effect):
                    self.world.add_component(action.target, copy.copy(component))

                if isinstance(component, Text):
                    self.messages.add("You throw the " + component.noun + " at the " + target_text.noun + ".")

            inventory.items.remove(action.item)
            self.world.delete_entity(action.item)

            actor.energy -= action.cost
            self.world.remove_component(entity, ThrowAction)
