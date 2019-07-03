import tcod as libtcod
from game_states import GameStates
from input_handlers import handle_input
from entity import Entity, get_blocking_entities_at_location
from render import clear_all, render_all
from game_map import GameMap
from fov import initialize_fov, recompute_fov


def main():
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

    player = Entity(0, 0, '@', libtcod.white, 'Player', True)
    entities = [player]

    libtcod.console_set_custom_font('data/arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    root = libtcod.console_init_root(screen_width, screen_height, 'Ghost Town', False, renderer, vsync=True)
    con = libtcod.console.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)
    player.x = game_map.rooms[0].center().x
    player.y = game_map.rooms[0].center().y

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    game_state = GameStates.PLAYERS_TURN
    running = True
    while running:
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False
        
        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_input()

        move = action.get('move')
        leave = action.get('exit')
        fullscreen = action.get('fullscreen')

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity != player:
                    print('The ' + entity.name + ' ponders the meaning of its existence.')

            game_state = GameStates.PLAYERS_TURN

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    print('You kick the ' + target.name + ' in the shins, much to it''s annoyance!')
                else:
                    player.move(dx, dy)
                    fov_recompute = True
                
                game_state = GameStates.ENEMY_TURN

        if leave:
            running = False
        
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()