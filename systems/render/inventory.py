import logging

import esper
import tcod as libtcod

from components import Player, Text, Inventory


class RenderInventorySystem(esper.Processor):
    def __init__(self, config, consoles, message_log):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.config = config
        self.consoles = consoles
        self.messages = message_log

        self.consoles.inventory = libtcod.console.Console(self.config.ui.width, self.config.ui.height)
        self.log.debug("Initialized!")

    def process(self):
        self.clear_buffer()
        self.render_ui()

        if self.config.ui.debug_position:
            self.render_debug()

    def render_ui(self):
        libtcod.console_set_default_foreground(self.consoles.ui, libtcod.white)

        x = 0
        y = 0

        for entity, (inventory, player) in self.world.get_components(Inventory, Player):
            self.draw_inventory(x, y, inventory)

    def clear_buffer(self):
        libtcod.console_set_default_background(self.consoles.inventory, libtcod.black)
        libtcod.console_clear(self.consoles.inventory)

    def draw(self, x, y, char, color):
        libtcod.console_set_default_foreground(self.consoles.inventory, color)
        libtcod.console_put_char(self.consoles.inventory, x, y, char, libtcod.BKGND_NONE)

    def render_debug(self):
        self.draw(0, 0, 'I', libtcod.red)
        self.draw(self.config.ui.width - 1, 0, 'I', libtcod.red)
        self.draw(0, self.config.ui.height - 1, 'I', libtcod.red)
        self.draw(self.config.ui.width - 1, self.config.ui.height - 1, 'I', libtcod.red)

    def draw_inventory(self, x, y, inventory):
        width = 15
        height = 15
        libtcod.console_rect(self.consoles.inventory, x, y, width, height, True)

        self.draw_text(" Inventory ", x, y)
        y += 2
        for idx in range(0, inventory.limit):
            if idx < len(inventory.items):
                item = inventory.items[idx]
                item_text = self.world.component_for_entity(item, Text)
                self.draw_text(chr(ord('a') + idx) + ". " + item_text.description, x, y)
            else:
                self.draw_text(chr(ord('a') + idx) + ". ", x, y)

            y += 1

    def draw_text(self, text, x, y, align=libtcod.LEFT):
        libtcod.console_print_ex(self.consoles.inventory, x, y, libtcod.BKGND_NONE, align, text)
