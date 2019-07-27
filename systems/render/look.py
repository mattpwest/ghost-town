import logging

import esper
import tcod as libtcod

from components import Text, Position, Target, Render, Health
from .util import draw_bar


class RenderLookSystem(esper.Processor):
    def __init__(self, game_map, consoles, config):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.map = game_map
        self.consoles = consoles
        self.consoles_map = consoles.layers["map"]
        self.consoles_ui = consoles.layers["ui"]
        self.config = config

        self.log.debug("Initialized!")

    def process(self):
        target = None
        for entity, (position, render, target) in self.world.get_components(Position, Render, Target):
            libtcod.console_set_char_background(self.consoles_map.console, position.x, position.y, render.color,
                                                libtcod.BKGND_SET)
            target = position

        if target is None:
            return

        x = self.config.ui.bar_width + 3
        y = 0
        w = self.config.ui.width - x
        h = self.config.ui.height
        self.consoles_ui.console.draw_rect(
            x,
            y,
            w,
            h,
            ord(" "),
            fg=libtcod.black,
            bg=libtcod.black,
            bg_blend=libtcod.BKGND_SET
        )

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
            draw_bar(
                self.consoles_ui.console,
                x + 2,
                y,
                'HP',
                health.points,
                health.maximum,
                self.config.ui.bar_width,
                libtcod.light_red, libtcod.darker_red
            )

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

    def draw_text(self, text, x, y, align=libtcod.LEFT):
        libtcod.console_print_ex(self.consoles_ui.console, x, y, libtcod.BKGND_NONE, align, text)
