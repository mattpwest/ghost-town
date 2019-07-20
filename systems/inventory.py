import logging

import esper
import tcod as libtcod

from components import Fighter, Attack, PickupAction, Inventory, Item, Text
from components.actor import Actor
from components.position import Position


class InventorySystem(esper.Processor):
    def __init__(self, game):
        self.log = logging.getLogger("InventorySystem")
        self.log.setLevel(logging.INFO)

        self.map = game.map
        self.messages = game.messages

    def process(self):
        for entity, (actor, position, inventory, action) \
                in self.world.get_components(Actor, Position, Inventory, PickupAction):

            if len(inventory.items) >= inventory.limit:
                self.messages.add('You don''t have room for that item!', libtcod.orange)
                self.world.remove_component(entity, PickupAction)
                return

            items = self.map.items[position.x][position.y]
            if len(items) == 0:
                self.messages.add('There is nothing to pick up here...')
                self.world.remove_component(entity, PickupAction)
                return

            item_entity = items.pop()
            inventory.items.append(item_entity)
            self.world.remove_component(item_entity, Item)  # Stop rendering on map
            item_text = self.world.component_for_entity(item_entity, Text)
            self.messages.add('You pick up the ' + item_text.noun + ' and add it to your pack.')
            self.log.info("Inventory: " + str(inventory.items))

            actor.energy -= action.cost
            self.world.remove_component(entity, PickupAction)

    def generate_attack(self, from_entity, to_entity):
        if self.world.has_component(from_entity, Fighter) and self.world.has_component(to_entity, Fighter):
            self.world.add_component(to_entity, Attack(from_entity))
