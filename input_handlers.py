import tcod as libtcod
import tcod.event
import tcod.event_constants as keys


def handle_input():
    result = {}
    
    for event in tcod.event.get():
        if event.type == "QUIT":
            result.update({'exit': True})
        elif event.type == "KEYDOWN":
            result.update(handle_keys(event))
    
    return result


def handle_keys(event):
    if event.sym == keys.K_UP:
        return {'move': (0, -1)}
    elif event.sym == keys.K_DOWN:
        return {'move': (0, 1)}
    elif event.sym == keys.K_LEFT:
        return {'move': (-1, 0)}
    elif event.sym == keys.K_RIGHT:
        return {'move': (1, 0)}

    if event.sym == keys.K_RETURN and event.mod & tcod.event.KMOD_ALT:
        return {'fullscreen': True}
    elif event.sym == keys.K_ESCAPE:
        return {'exit': True}

    return {}
