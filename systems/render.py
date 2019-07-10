import esper
import tcod as libtcod

from components import Position, Render, Viewable


class RenderSystem(esper.Processor):
    def __init__(self, world, screen_width, screen_height, renderer):
        self.world = world
        self.screen_width = screen_width
        self.screen_height = screen_height

        libtcod.console_set_custom_font('data/arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
        self.root = libtcod.console_init_root(screen_width, screen_height, 'Ghost Town', False, renderer, vsync=True)
        self.con = libtcod.console.Console(screen_width, screen_height)
    
    def process(self):
        for entity, (position, render, viewable) in self.world.get_components(Position, Render, Viewable):
            #print("Drawing entity: " + str(entity) + " (x=" + str(position.x) + ", y=" + str(position.y) + ", char=" + render.char + ", color=" + str(render.color) + ")")

            if viewable.lit:
                self.draw(position, render.char, render.color)

                viewable.explored = True
            elif viewable.explored:
                self.draw(position, render.char, render.color * libtcod.Color(50, 50, 50))

        libtcod.console_blit(self.con, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
        libtcod.console_flush()

        for entity, (position, render, viewable) in self.world.get_components(Position, Render, Viewable):
            if viewable.visible or viewable.explored:
                self.clear(position)

    def draw(self, position, char, color):
        libtcod.console_set_default_foreground(self.con, color)
        libtcod.console_put_char(self.con, position.x, position.y, char, libtcod.BKGND_NONE)

    def clear(self, position):
        libtcod.console_put_char(self.con, position.x, position.y, ' ', libtcod.BKGND_NONE)

    def render_all(self, con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
        if fov_recompute:
            for y in range(game_map.height):
                for x in range(game_map.width):
                    visible = libtcod.map_is_in_fov(fov_map, x, y)
                    wall = game_map.tiles[x][y].block_sight

                    if visible:
                        if wall:
                            libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)

                        game_map.tiles[x][y].explored = True
                    elif game_map.tiles[x][y].explored:
                        if wall:
                            libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

        for entity in entities:
            self.draw_entity(con, entity, fov_map)

        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    def clear_all(self, con, entities):
        for entity in entities:
            self.clear_entity(con, entity)

    def draw_entity(self, con, entity, fov_map):
        if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            libtcod.console_set_default_foreground(con, entity.color)
            libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

    def clear_entity(self, con, entity):
        libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)