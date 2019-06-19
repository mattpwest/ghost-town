import tcod as libtcod
from input_handlers import handle_input
from tcod.tcod import _int

def main():
    renderer = libtcod.RENDERER_SDL2
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    libtcod.console_set_custom_font('data/arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    root = libtcod.console_init_root(screen_width, screen_height, 'Ghost Town', False, renderer, vsync=True)

    con = libtcod.console.Console(screen_width, screen_height)
    con.default_fg = libtcod.white
    running = True
    while running:
        #libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        con.put_char(player_x, player_y, _int('@'), libtcod.BKGND_NONE)
        #ibtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        con.blit(dest=root, dest_x=0, dest_y=0, width=screen_width, height=screen_height, fg_alpha=255, bg_alpha=255, key_color=0)

        libtcod.console_flush()

        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

        action = handle_input()

        move = action.get('move')
        leave = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if leave:
            running = False
        
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()