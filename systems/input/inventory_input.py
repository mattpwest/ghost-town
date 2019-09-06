import copy
import logging
from enum import auto, Enum

import esper
import tcod.event
import tcod.event_constants as keys

from components import Player, InventoryAction, TargetType, Position, Target
from states import State, Inventory


class InventoryInputSystem(esper.Processor):
    def __init__(self, game_map, game_state, entity_factory):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.mode = Mode.ITEMS

        self.map = game_map
        self.game = game_state
        self.entity_factory = entity_factory

    def process(self):
        action = get_input_non_blocking()

        if action is not None and action["quit"]:
            self.game.new_state = State.MAP

        no_inventory = True
        for player, (unused, inventory) in self.world.get_components(Player, Inventory):
            no_inventory = False

            if action is None:
                continue

            if action["mode"] is not None:
                self.mode = action["mode"]

                if self.mode == Mode.ACTIONS:
                    inventory.selected_action = 0
                elif self.mode == Mode.ITEMS:
                    inventory.selected_action = -1

            if action["activate"] and self.mode == Mode.ACTIONS:
                item = inventory.items[inventory.selected]
                actions = []
                for component in self.world.components_for_entity(item):
                    if isinstance(component, InventoryAction):
                        actions.append(component)

                action = actions[inventory.selected_action]
                action_to_execute = copy.copy(action)
                if action_to_execute.target_type == TargetType.SELF:
                    action_to_execute.target = player
                    self.world.add_component(player, action_to_execute)
                else:
                    position = self.world.component_for_entity(player, Position)
                    target = self.entity_factory.target(position.x, position.y)
                    self.world.component_for_entity(target, Target).action = action_to_execute

                    # Exit inventory, go to LOOK state, reset selections for next inventory activation
                    inventory.selected = -1
                    inventory.selected_action = -1
                    self.game.new_state = State.LOOK
                    return

                # Exit inventory, reset selections for next activation
                self.game.new_state = State.MAP
                inventory.selected = -1
                inventory.selected_action = -1

                continue

            selection_delta = action["select"]
            if selection_delta == 0:
                continue

            if self.mode == Mode.ITEMS and 0 <= inventory.selected + selection_delta < len(inventory.items):
                inventory.selected += selection_delta
            elif self.mode == Mode.ACTIONS and inventory.selected_action + selection_delta >= 0:
                inventory.selected_action += selection_delta

        # Bit of a hack: oops character died while showing the inventory, go back to map state
        if no_inventory:
            self.game.new_state = State.MAP


def get_input_non_blocking():
    result = None

    for event in tcod.event.get():
        if event.type == 'KEYDOWN':
            result = handle_keys(event)

    return result


def handle_keys(event):
    if event.sym == keys.K_UP:
        return select(-1)
    elif event.sym == keys.K_DOWN:
        return select(1)
    elif event.sym == keys.K_LEFT:
        return mode(Mode.ITEMS)
    elif event.sym == keys.K_RIGHT:
        return mode(Mode.ACTIONS)
    elif event.sym == keys.K_RETURN:
        return activate()
    elif event.sym == keys.K_ESCAPE:
        return {"select": 0, "mode": None, "quit": True, "activate": False}

    return None


def select(change):
    return {"select": change, "mode": None, "quit": False, "activate": False}


def mode(modus):
    return {"select": 0, "mode": modus, "quit": False, "activate": False}


def activate():
    return {"select": 0, "mode": None, "quit": False, "activate": True}


class Mode(Enum):
    ITEMS = auto()
    ACTIONS = auto()
