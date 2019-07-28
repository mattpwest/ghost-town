import logging

import esper
import tcod as libtcod

from components import Player, Text, Inventory, Action
from systems.render.consoles import ConsoleLayer, ConsoleRect, ConsolePoint


class RenderInventorySystem(esper.Processor):
    def __init__(self, config, consoles, message_log):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.config = config
        self.consoles = consoles
        self.messages = message_log

        width = self.config.inventory.width
        height = self.config.inventory.height
        self.consoles_inventory = ConsoleLayer(
            libtcod.console.Console(width * 2, height),
            priority=3,
            name="inventory",
            from_rect=ConsoleRect(0, 0, width * 2, height),
            to_point=ConsolePoint(0, 0)
        )
        self.consoles.add_layer(self.consoles_inventory)
        self.consoles.disable_layer(self.consoles_inventory)

        self.BACKGROUND_COLOR = libtcod.desaturated_blue * 0.5
        self.FOREGROUND_COLOR = libtcod.desaturated_blue
        self.SELECTED_COLOR = libtcod.desaturated_blue * 1.5

        self.log.debug("Initialized!")

    def process(self):
        self._clear_buffer()
        self._render_ui()

        if self.config.ui.debug_position:
            self._render_debug()

    def _render_ui(self):
        libtcod.console_set_default_foreground(self.consoles_inventory.console, libtcod.white)

        x = 0
        y = 0

        for entity, (inventory, player) in self.world.get_components(Inventory, Player):
            self._draw_inventory(x, y, inventory)

    def _clear_buffer(self):
        libtcod.console_set_default_background(self.consoles_inventory.console, libtcod.black)
        libtcod.console_clear(self.consoles_inventory.console)

    def _draw(self, x, y, char, color):
        libtcod.console_set_default_foreground(self.consoles_inventory.console, color)
        libtcod.console_put_char(self.consoles_inventory.console, x, y, char, libtcod.BKGND_NONE)

    def _render_debug(self):
        self._draw(0, 0, 'I', libtcod.red)
        self._draw(self.config.ui.width - 1, 0, 'I', libtcod.red)
        self._draw(0, self.config.ui.height - 1, 'I', libtcod.red)
        self._draw(self.config.ui.width - 1, self.config.ui.height - 1, 'I', libtcod.red)

    def _draw_inventory(self, x, y, inventory):
        width = self.config.inventory.width
        height = self.config.inventory.height
        self._draw_panel_background(x, y, width, height, self.BACKGROUND_COLOR)

        self._draw_text(" Inventory ", x + int(width / 2), y, libtcod.CENTER)
        y += 2

        for idx in range(0, inventory.limit):
            if idx < len(inventory.items):
                if inventory.selected == idx:
                    self._highlight_slot(y, width)
                    self._draw_item_details(idx, inventory, y - 1, width)

                self._draw_item(idx, inventory, x, y)
            else:
                self._draw_empty_slot(idx, x, y)

            y += 1

        libtcod.console_set_default_foreground(self.consoles_inventory.console, libtcod.white)

    def _draw_panel_background(self, x, y, width, height, color):
        libtcod.console_set_default_background(self.consoles_inventory.console, color)
        libtcod.console_rect(self.consoles_inventory.console, x, y, width, height, True, libtcod.BKGND_SCREEN)

    def _highlight_slot(self, y, width):
        libtcod.console_set_default_background(self.consoles_inventory.console, self.FOREGROUND_COLOR)
        libtcod.console_rect(self.consoles_inventory.console, 0, y, width, 1, True, libtcod.BKGND_SET)
        libtcod.console_set_default_background(self.consoles_inventory.console, self.BACKGROUND_COLOR)

    def _draw_item_details(self, idx, inventory, y, width):
        item = inventory.items[idx]
        actions = []
        for component in self.world.components_for_entity(item):
            if isinstance(component, Action):
                actions.append(component)

        num_actions = len(actions)
        num_details = 3
        self._draw_panel_background(width, y, width, num_actions + num_details + 1, self.FOREGROUND_COLOR)

        self._draw_text("ACTIONS", width + int(width / 2), y, libtcod.CENTER)
        y += 1

        for idx_action in range(0, len(actions)):
            action = actions[idx_action]
            if idx_action == inventory.selected_action:
                libtcod.console_set_default_background(self.consoles_inventory.console, self.SELECTED_COLOR)
                libtcod.console_rect(self.consoles_inventory.console, width, y, width, 1, True, libtcod.BKGND_SET)
                libtcod.console_set_default_background(self.consoles_inventory.console, self.FOREGROUND_COLOR)

                self._draw_text(action.name, width + 1, y)
            else:
                self._draw_text(action.name, width + 1, y)

            y += 1

        y += 1
        self._draw_text("DESCRIPTION", width + int(width / 2), y, libtcod.CENTER)

        y += 1
        item_text = self.world.component_for_entity(inventory.items[idx], Text)
        self._draw_text(item_text.description, width + 1, y)

    def _draw_item(self, idx, inventory, x, y):
        item = inventory.items[idx]
        item_text = self.world.component_for_entity(item, Text)
        libtcod.console_set_default_foreground(self.consoles_inventory.console, libtcod.white)
        self._draw_text(" " + chr(ord('a') + idx) + ". " + item_text.pronoun + " " + item_text.noun, x, y)

    def _draw_empty_slot(self, idx, x, y):
        libtcod.console_set_default_foreground(self.consoles_inventory.console, libtcod.gray)
        self._draw_text(" " + chr(ord('a') + idx) + ". ", x, y)

    def _draw_text(self, text, x, y, align=libtcod.LEFT):
        libtcod.console_print_ex(self.consoles_inventory.console, x, y, libtcod.BKGND_NONE, align, text)
