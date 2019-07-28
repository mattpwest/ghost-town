import logging

import esper

from components import Inventory, Item, Text, DropAction
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
