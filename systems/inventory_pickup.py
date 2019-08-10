import logging

import esper
import tcod as libtcod

from components import PickupAction, Inventory, Item, Text
from components.actor import Actor
from components.position import Position


class InventoryPickupSystem(esper.Processor):
    def __init__(self, game_map, message_log):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.map = game_map
        self.messages = message_log

    def process(self):
        for entity, (actor, position, inventory, action) \
                in self.world.get_components(Actor, Position, Inventory, PickupAction):

            if not self.map.has_item(position.x, position.y):
                self.messages.add("There is nothing to pick up here...")
                self.world.remove_component(entity, PickupAction)
                return

            if len(inventory.items) >= inventory.limit:
                self.messages.add("You don't have room for that item!", libtcod.orange)
                self.world.remove_component(entity, PickupAction)
                return

            item_entity = self.map.take_item(position.x, position.y)
            inventory.items.append(item_entity)
            item_text = self.world.component_for_entity(item_entity, Text)
            self.messages.add("You pick up the " + item_text.noun + " and add it to your pack.")
            self.log.info("Inventory: " + str(inventory.items))

            actor.energy -= action.cost
            self.world.remove_component(entity, PickupAction)
