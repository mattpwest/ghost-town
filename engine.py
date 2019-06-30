import tcod as libtcod
from input_handlers import handle_input
from entity import Entity
from render import clear_all, render_all
from game_map import GameMap


def main():
    renderer = libtcod.RENDERER_SDL2
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    colors = {
       'dark_wall': libtcod.Color(0, 0, 100),
       'dark_ground': libtcod.Color(50, 50, 150)
    }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2 - 5), '@', libtcod.yellow)
    entities = [player, npc]

    libtcod.console_set_custom_font('data/arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    root = libtcod.console_init_root(screen_width, screen_height, 'Ghost Town', False, renderer, vsync=True)
    con = libtcod.console.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)

    running = True
    while running:
        render_all(con, entities, game_map, screen_width, screen_height, colors)
        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_input()

        move = action.get('move')
        leave = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move

            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if leave:
            running = False
        
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()