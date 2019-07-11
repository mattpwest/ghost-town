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
    fov_radius = 5

    max_monsters_per_room = 3

    game_state = {'running': True}

    world = esper.World()

    factory = EntityFactory(world)

    game_map = GameMap(map_width, map_height, world, factory)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, max_monsters_per_room)

    world.add_processor(systems.MovementSystem(game_map), 10)
    world.add_processor(systems.FreeActionsSystem(game_state), 10)
    world.add_processor(systems.CombatSystem(), 9)
    world.add_processor(systems.DamageSystem(game_map), 8)
    world.add_processor(systems.VisionSystem(screen_width, screen_height, fov_radius), 6)
    world.add_processor(systems.RenderSystem(world, screen_width, screen_height, renderer), 5)
    world.add_processor(systems.ActionSystem(game_state), 1)

    pentity = factory.player(game_map.rooms[0].center().x, game_map.rooms[0].center().y)

    while game_state['running']:
        world.process()


if __name__ == '__main__':
    main()