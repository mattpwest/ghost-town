import logging

import esper
import tcod as libtcod

from components import Player, Text, Health
from systems.render.consoles import ConsoleLayer, ConsoleRect, ConsolePoint
from .util import draw_bar


class RenderUiSystem(esper.Processor):
    def __init__(self, config, consoles, message_log):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.config = config
        self.consoles = consoles
        self.messages = message_log

        self.consoles_ui = ConsoleLayer(
            libtcod.console.Console(self.config.ui.width, self.config.ui.height),
            priority=2,
            name="ui",  # TODO: Rename this to HUD
            from_rect=ConsoleRect(0, 0, self.config.ui.width, self.config.ui.height),
            to_point=ConsolePoint(0, self.config.display.height - self.config.ui.height)
        )
        self.consoles.add_layer(self.consoles_ui)

        self.log.debug("Initialized!")

    def process(self):
        self.clear_buffer()
        self.render_ui()

        if self.config.ui.debug_position:
            self.render_debug()

    def render_ui(self):
        libtcod.console_set_default_foreground(self.consoles_ui.console, libtcod.white)

        x = 1
        y = 1
        for entity, (text, health, player) in self.world.get_components(Text, Health, Player):
            draw_bar(
                self.consoles_ui.console,
                x,
                y,
                'HP',
                health.points,
                health.maximum,
                self.config.ui.bar_width,
                libtcod.light_red,
                libtcod.darker_red
            )

        self.draw_messages(self.config.ui.bar_width + 3)

    def clear_buffer(self):
        libtcod.console_set_default_background(self.consoles_ui.console, libtcod.black)
        libtcod.console_clear(self.consoles_ui.console)

    def draw(self, x, y, char, color):
        libtcod.console_set_default_foreground(self.consoles_ui.console, color)
        libtcod.console_put_char(self.consoles_ui.console, x, y, char, libtcod.BKGND_NONE)

    def render_debug(self):
        self.draw(0, 0, 'U', libtcod.red)
        self.draw(self.config.ui.width - 1, 0, 'U', libtcod.red)
        self.draw(0, self.config.ui.height - 1, 'U', libtcod.red)
        self.draw(self.config.ui.width - 1, self.config.ui.height - 1, 'U', libtcod.red)

    def draw_messages(self, x):
        y = 1
        size = self.config.ui.height - y

        console = self.consoles_ui.console

        messages = self.messages.log[-size:]
        color = None
        for idx in range(0, len(messages)):
            if color != messages[idx].color:
                color = messages[idx].color
                libtcod.console_set_default_foreground(console, color)

            self.draw_text(messages[idx].text, x, y + idx)

        libtcod.console_set_default_foreground(self.consoles_ui.console, libtcod.white)

    def draw_text(self, text, x, y, align=libtcod.LEFT):
        libtcod.console_print_ex(self.consoles_ui.console, x, y, libtcod.BKGND_NONE, align, text)
