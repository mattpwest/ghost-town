import logging

import esper
import tcod as libtcod

from components import Player, Text, Inventory
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
            libtcod.console.Console(width, height),
            priority=3,
            name="inventory",
            from_rect=ConsoleRect(0, 0, width, height),
            to_point=ConsolePoint(0, 0)
        )
        self.consoles.add_layer(self.consoles_inventory)
        self.consoles.disable_layer(self.consoles_inventory)

        self.log.debug("Initialized!")

    def process(self):
        self.clear_buffer()
        self.render_ui()

        if self.config.ui.debug_position:
            self.render_debug()

    def render_ui(self):
        libtcod.console_set_default_foreground(self.consoles_inventory.console, libtcod.white)

        x = 0
        y = 0

        for entity, (inventory, player) in self.world.get_components(Inventory, Player):
            self.draw_inventory(x, y, inventory)

    def clear_buffer(self):
        libtcod.console_set_default_background(self.consoles_inventory.console, libtcod.black)
        libtcod.console_clear(self.consoles_inventory.console)

    def draw(self, x, y, char, color):
        libtcod.console_set_default_foreground(self.consoles_inventory.console, color)
        libtcod.console_put_char(self.consoles_inventory.console, x, y, char, libtcod.BKGND_NONE)

    def render_debug(self):
        self.draw(0, 0, 'I', libtcod.red)
        self.draw(self.config.ui.width - 1, 0, 'I', libtcod.red)
        self.draw(0, self.config.ui.height - 1, 'I', libtcod.red)
        self.draw(self.config.ui.width - 1, self.config.ui.height - 1, 'I', libtcod.red)

    def draw_inventory(self, x, y, inventory):
        width = self.config.inventory.width
        height = self.config.inventory.height
        libtcod.console_set_default_background(self.consoles_inventory.console, libtcod.desaturated_blue)
        libtcod.console_rect(self.consoles_inventory.console, x, y, width, height, True, libtcod.BKGND_SCREEN)

        self.draw_text(" Inventory ", x + int(width / 2), y, libtcod.CENTER)
        y += 2
        for idx in range(0, inventory.limit):
            if idx < len(inventory.items):
                item = inventory.items[idx]
                item_text = self.world.component_for_entity(item, Text)
                libtcod.console_set_default_foreground(self.consoles_inventory.console, libtcod.white)
                self.draw_text(" " + chr(ord('a') + idx) + ". " + item_text.pronoun + " " + item_text.noun, x, y)
            else:
                libtcod.console_set_default_foreground(self.consoles_inventory.console, libtcod.gray)
                self.draw_text(" " + chr(ord('a') + idx) + ". ", x, y)

            y += 1

        libtcod.console_set_default_foreground(self.consoles_inventory.console, libtcod.white)

    def draw_text(self, text, x, y, align=libtcod.LEFT):
        libtcod.console_print_ex(self.consoles_inventory.console, x, y, libtcod.BKGND_NONE, align, text)
