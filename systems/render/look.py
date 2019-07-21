import logging

import esper
import tcod as libtcod

from components import Text, Position, Target, Render, Health


class RenderLookSystem(esper.Processor):
    def __init__(self, game_map, consoles, config):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.map = game_map
        self.consoles = consoles
        self.config = config

        self.log.debug("Initialized!")

    def process(self):
        target = None
        for entity, (position, render, target) in self.world.get_components(Position, Render, Target):
            libtcod.console_set_char_background(self.consoles.map, position.x, position.y, render.color,
                                                libtcod.BKGND_SET)
            target = position

        if target is None:
            return

        x = self.config.ui.bar_width + 3
        y = 0
        w = self.config.ui.width - x
        h = self.config.ui.height
        self.consoles.ui.draw_rect(x, y, w, h, ord(" "), fg=libtcod.black, bg=libtcod.black, bg_blend=libtcod.BKGND_SET)

        creature = self.map.entities[target.x][target.y]
        self.log.debug("Look creature: " + str(creature))
        if creature is not None:
            self.draw_creature(creature)
            return

        items = self.map.items[target.x][target.y]
        self.log.debug("Look items: " + str(creature))
        if items is not None and len(items) > 0:
            self.draw_items(items)
            return

        tile = self.map.tiles[target.x][target.y]
        self.log.debug("Look tile: " + str(tile))
        if tile is not None:
            self.draw_tile(tile)

    def draw_creature(self, creature):
        x = self.config.ui.bar_width + 3
        y = 1
        for text in self.world.try_component(creature, Text):
            self.draw_text(text.description, x, y)

        y += 1
        for health in self.world.try_component(creature, Health):
            self.draw_bar(x + 2, y, 'HP', health.points, health.maximum, libtcod.light_red, libtcod.darker_red)

    def draw_items(self, items):
        x = self.config.ui.bar_width + 3
        y = 1

        message = "There "
        if len(items) == 1:
            message += "is an item here:"
        else:
            message += "are several items here:"
        self.draw_text(message, x, y)
        y += 1

        for item in items:
            self.log.debug("\tItem: " + str(item))
            for text in self.world.try_component(item, Text):
                self.log.debug("\t\tText:" + str(text))
                self.draw_text(" - " + text.description, x, y)
                y += 1

    def draw_tile(self, tile):
        x = self.config.ui.bar_width + 3
        y = 1
        for text in self.world.try_component(tile, Text):
            self.draw_text(text.description, x, y)

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

    def draw_text(self, text, x, y, align=libtcod.LEFT):
        libtcod.console_print_ex(self.consoles.ui, x, y, libtcod.BKGND_NONE, align, text)
