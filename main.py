import logging

import esper
import tcod as libtcod

import systems as systems
from entities import EntityFactory
from game_map import GameMap


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
    logging.root.setLevel(logging.INFO)

    renderer = libtcod.RENDERER_SDL2
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    #player = Entity(0, 0, '@', libtcod.white, 'Player', True)
    #entities = [player]

    #libtcod.console_set_custom_font('data/arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    #root = libtcod.console_init_root(screen_width, screen_height, 'Ghost Town', False, renderer, vsync=True)
    #con = libtcod.console.Console(screen_width, screen_height)

    game_state = {'running': True}

    world = esper.World()

    factory = EntityFactory(world)

    game_map = GameMap(map_width, map_height, world, factory)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, max_monsters_per_room)

    world.add_processor(systems.MovementSystem(game_map), 10)
    world.add_processor(systems.FreeActionsSystem(game_state), 10)
    world.add_processor(systems.RenderSystem(world, screen_width, screen_height, renderer), 5)
    world.add_processor(systems.ActionSystem(game_state), 1)

    #player.x = game_map.rooms[0].center().x
    #player.y = game_map.rooms[0].center().y

    #fov_recompute = True
    #fov_map = initialize_fov(game_map)

    pentity = factory.player(game_map.rooms[0].center().x, game_map.rooms[0].center().y)

    while game_state['running']:
        world.process()
        # #if fov_recompute:
        # #    recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
        #
        # #render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        # #fov_recompute = False
        #
        # #libtcod.console_flush()
        #
        # #clear_all(con, entities)
        #
        # action = handle_input()
        #
        # move = action.get('move')
        # leave = action.get('exit')
        # fullscreen = action.get('fullscreen')
        #
        # # if game_state == GameStates.ENEMY_TURN:
        # #     for entity in entities:
        # #         if entity != player:
        # #             print('The ' + entity.name + ' ponders the meaning of its existence.')
        # #
        # #     game_state = GameStates.PLAYERS_TURN
        #
        # if move and game_state == GameStates.PLAYERS_TURN:
        #     dx, dy = move
        #     #destination_x = player.x + dx
        #     #destination_y = player.y + dy
        #     #
        #     # if not game_map.is_blocked(destination_x, destination_y):
        #     #     target = get_blocking_entities_at_location(entities, destination_x, destination_y)
        #     #
        #     #     if target:
        #     #         print('You kick the ' + target.name + ' in the shins, much to it''s annoyance!')
        #     #     else:
        #     #         player.move(dx, dy)
        #     #         fov_recompute = True
        #
        #     game_state = GameStates.ENEMY_TURN
        #
        # if leave:
        #     running = False
        #
        # if fullscreen:
        #     libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()