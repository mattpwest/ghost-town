import esper
import tcod as libtcod

from components import Position, Viewable, Tangible, Player


class VisionSystem(esper.Processor):
    def __init__(self, screen_width, screen_height, view_radius):
        self.width = screen_width
        self.height = screen_height
        self.radius = view_radius

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

            self.recompute_fov(self.x, self.y, self.radius)

    def initialize_fov(self):
        fov_map = libtcod.map_new(self.width, self.height)

        for entity, (position, tangible, viewable) in self.world.get_components(Position, Tangible, Viewable):
            transparent = not tangible.blocks_physical

            libtcod.map_set_properties(
                fov_map,
                position.x,
                position.y,
                transparent,
                transparent
            )

        return fov_map

    def recompute_fov(self, x, y, radius, light_walls=True, algorithm=0):
        libtcod.map_compute_fov(self.fov_map, x, y, radius, light_walls, algorithm)

        for entity, (position, viewable) in self.world.get_components(Position, Viewable):
            viewable.lit = self.fov_map.fov[position.y, position.x]