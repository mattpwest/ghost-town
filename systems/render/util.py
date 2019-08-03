import tcod as libtcod


def draw_bar(console, x, y, name, value, maximum, bar_width, bar_color, back_color):
    total_width = bar_width

    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(console, back_color)
    libtcod.console_rect(console, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(console, bar_color)
    if bar_width > 0:
        libtcod.console_rect(console, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(console, libtcod.white)
    if name is None:
        message = "{0}/{1}".format(value, maximum)
    else:
        message = "{0}: {1}/{2}".format(name, value, maximum)
    libtcod.console_print_ex(console, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER, message)
