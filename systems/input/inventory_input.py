import copy
import logging
from enum import auto, Enum

import esper
import tcod.event
import tcod.event_constants as keys

from components import Player, Action
from states import State, Inventory


class InventoryInputSystem(esper.Processor):
    def __init__(self, game_map, game_state):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.map = game_map
        self.game = game_state
        self.mode = Mode.ITEMS

    def process(self):
        action = handle_input()

        if action["quit"]:
            self.game.new_state = State.MAP

        for player, (unused, inventory) in self.world.get_components(Player, Inventory):
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
                    if isinstance(component, Action):
                        actions.append(component)

                action = actions[inventory.selected_action]
                self.world.add_component(player, copy.copy(action))

                # Exit inventory, reset selections for next activation
                self.game.new_state = State.MAP
                inventory.selected = -1
                inventory.selected_action = -1

                # TODO: Deal with targeted actions...

                # if action.can_target.__contains__(TargetTypes.SELF):
                #     self.world.add_component(player, )
                continue

            selection_delta = action["select"]
            if selection_delta == 0:
                continue

            if self.mode == Mode.ITEMS and 0 <= inventory.selected + selection_delta < len(inventory.items):
                inventory.selected += selection_delta
            elif self.mode == Mode.ACTIONS and inventory.selected_action + selection_delta >= 0:
                inventory.selected_action += selection_delta


def handle_input():
    result = None

    while result is None:
        for event in tcod.event.wait():
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

    return {"select": 0, "mode": None, "quit": False, "activate": False}


def select(change):
    return {"select": change, "mode": None, "quit": False, "activate": False}


def mode(modus):
    return {"select": 0, "mode": modus, "quit": False, "activate": False}


def activate():
    return {"select": 0, "mode": None, "quit": False, "activate": True}


class Mode(Enum):
    ITEMS = auto()
    ACTIONS = auto()
