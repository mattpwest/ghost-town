import logging

import esper
import tcod as libtcod

from components import Position, Optics, Tangible, Player


class VisionSystem(esper.Processor):
    def __init__(self, config):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

        self.config = config

        self.fov_map = None
        self.x = -1
        self.y = -1

    def process(self):
        if self.fov_map is None:
            self.fov_map = self.initialize_fov()

        player = None
        for entity, (position, player) in self.world.get_components(Position, Player):
            player = position

        if player is not None and (player.x != self.x or player.y != self.y):
            self.x = player.x
            self.y = player.y

            self.recompute_fov(self.x, self.y)

    def initialize_fov(self):
        self.log.debug("Initializing FOV map...")
        fov_map = libtcod.map_new(self.config.map.width, self.config.map.height)

        for entity, (position, optics) in self.world.get_components(Position, Optics):
            fov_map.transparent[position.y][position.x] = optics.transparent

        return fov_map

    def recompute_fov(self, x, y):
        self.log.debug("Recomputing FOV map...")
        radius = self.config.vision.radius
        light_walls = self.config.vision.light_walls
        algorithm = self.config.vision.algorithm

        libtcod.map_compute_fov(self.fov_map, x, y, radius, light_walls, algorithm)

        for entity, (position, optics) in self.world.get_components(Position, Optics):
            optics.lit = self.fov_map.fov[position.y, position.x] or self.config.vision.debug

            if optics.lit:
                optics.explored = True
