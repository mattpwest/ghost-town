import logging

import esper
import tcod as libtcod

from systems.render.consoles import ConsoleLayer, ConsoleRect, ConsolePoint


class RenderMenuSystem(esper.Processor):
    def __init__(self, config, consoles, game_state):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.config = config
        self.consoles = consoles
        self.game = game_state

        width = self.config.display.width
        height = self.config.display.height
        self.consoles_menu = ConsoleLayer(
            libtcod.console.Console(width, height),
            priority=4,
            name="menu",
            from_rect=ConsoleRect(0, 0, width, height),
            to_point=ConsolePoint(0, 0)
        )
        self.consoles.add_layer(self.consoles_menu)

        self.BACKGROUND_COLOR = libtcod.desaturated_blue * 0.5
        self.FOREGROUND_COLOR = libtcod.desaturated_blue
        self.SELECTED_COLOR = libtcod.desaturated_blue * 1.5

        self.log.debug("Initialized!")

    def process(self):
        self._clear_buffer()

        libtcod.console_set_default_foreground(self.consoles_menu.console, libtcod.white)

        x = 0
        y = 0

        y = self._draw_logo(x, y)
        y = self._draw_menu(x, y)

    def _clear_buffer(self):
        libtcod.console_set_default_background(self.consoles_menu.console, libtcod.black)
        libtcod.console_clear(self.consoles_menu.console)

    def _draw(self, x, y, char, color):
        libtcod.console_set_default_foreground(self.consoles_menu.console, color)
        libtcod.console_put_char(self.consoles_menu.console, x, y, char, libtcod.BKGND_NONE)

    def _draw_logo(self, x, y):
        y = y + 1

        libtcod.console_set_default_foreground(self.consoles_menu.console, libtcod.lightest_blue)
        self._draw_text(
            "Ghost Town",
            int(self.config.display.width / 2),
            y,
            libtcod.CENTER
        )

        y = y + 2
        return y

    def _draw_menu(self, x, y):
        libtcod.console_set_default_foreground(self.consoles_menu.console, libtcod.white)

        center = int(self.config.display.width / 2)
        for index in range(len(self.game.menus)):
            menu = self.game.menus[index]

            if self.game.menu_selected == index:
                self._draw_slot(center - 5, y, 10, self.SELECTED_COLOR)
                self._draw_text(menu["text"], center, y, libtcod.CENTER)
            else:
                self._draw_slot(center - 5, y, 10, self.FOREGROUND_COLOR)
                self._draw_text(menu["text"], center, y, libtcod.CENTER)
            y += 1

        return y + 1

    def _draw_panel_background(self, x, y, width, height, color):
        libtcod.console_set_default_background(self.consoles_menu.console, color)
        libtcod.console_rect(self.consoles_menu.console, x, y, width, height, True, libtcod.BKGND_SCREEN)

    def _draw_slot(self, x, y, width, color):
        libtcod.console_set_default_background(self.consoles_menu.console, color)
        libtcod.console_rect(self.consoles_menu.console, x, y, width, 1, True, libtcod.BKGND_SET)
        libtcod.console_set_default_background(self.consoles_menu.console, self.BACKGROUND_COLOR)

    def _draw_text(self, text, x, y, align=libtcod.LEFT):
        libtcod.console_print_ex(self.consoles_menu.console, x, y, libtcod.BKGND_NONE, align, text)
