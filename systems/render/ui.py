import logging

import esper
import tcod as libtcod

from components import Player, Text, Health


class RenderUiSystem(esper.Processor):
    def __init__(self, config, consoles, message_log):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.config = config
        self.consoles = consoles
        self.messages = message_log

        self.consoles.ui = libtcod.console.Console(self.config.ui.width, self.config.ui.height)
        self.log.debug("Initialized!")

    def process(self):
        self.clear_buffer()
        self.render_ui()

        if self.config.ui.debug_position:
            self.render_debug()

    def render_ui(self):
        libtcod.console_set_default_foreground(self.consoles.ui, libtcod.white)

        x = 1
        y = self.config.ui.height - 2
        for entity, (text, health, player) in self.world.get_components(Text, Health, Player):
            self.draw_bar(x, y, 'HP', health.points, health.maximum, libtcod.light_red, libtcod.darker_red)

        self.draw_messages(self.config.ui.bar_width + 3)

    def clear_buffer(self):
        libtcod.console_set_default_background(self.consoles.ui, libtcod.black)
        libtcod.console_clear(self.consoles.ui)

    def draw(self, x, y, char, color):
        libtcod.console_set_default_foreground(self.consoles.ui, color)
        libtcod.console_put_char(self.consoles.ui, x, y, char, libtcod.BKGND_NONE)

    def draw_bar(self, x, y, name, value, maximum, bar_color, back_color):
        console = self.consoles.ui
        total_width = self.config.ui.bar_width

        bar_width = int(float(value) / maximum * total_width)

        libtcod.console_set_default_background(console, back_color)
        libtcod.console_rect(console, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

        libtcod.console_set_default_background(console, bar_color)
        if bar_width > 0:
            libtcod.console_rect(console, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

        libtcod.console_set_default_foreground(console, libtcod.white)
        libtcod.console_print_ex(console, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                                 '{0}: {1}/{2}'.format(name, value, maximum))

    def render_debug(self):
        self.draw(0, 0, 'U', libtcod.red)
        self.draw(self.config.ui.width - 1, 0, 'U', libtcod.red)
        self.draw(0, self.config.ui.height - 1, 'U', libtcod.red)
        self.draw(self.config.ui.width - 1, self.config.ui.height - 1, 'U', libtcod.red)

    def draw_messages(self, x):
        y = 1
        size = self.config.ui.height - y

        console = self.consoles.ui

        messages = self.messages.log[-size:]
        color = None
        for idx in range(0, len(messages)):
            if color != messages[idx].color:
                color = messages[idx].color
                libtcod.console_set_default_foreground(console, color)

            self.draw_text(messages[idx].text, x, y + idx, )

    def draw_text(self, text, x, y, align=libtcod.LEFT):
        libtcod.console_print_ex(self.consoles.ui, x, y, libtcod.BKGND_NONE, align, text)
