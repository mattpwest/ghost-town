class Consoles:
    def __init__(self):
        self.root = None

        self.layers = {}
        self.layers_active = []

    def add_layer(self, layer):
        self.layers[layer.name] = layer

        if layer.active:
            self.layers_active.append(layer)
            self.layers_active.sort(key=by_priority)

    def remove_layer(self, layer):
        del self.layers[layer.name]
        self.layers_active.remove(layer)

    def disable_layer(self, layer):
        if not layer.active:
            return

        layer.active = False
        self.layers_active.remove(layer)

    def enable_layer(self, layer):
        if layer.active:
            return

        layer.active = True
        self.layers_active.append(layer)
        self.layers_active.sort(key=by_priority)


class ConsoleLayer:
    def __init__(self, console, priority, name, from_rect, to_point):
        self.console = console
        self.priority = priority
        self.name = name
        self.active = True
        self.from_rect = from_rect
        self.to_point = to_point


class ConsolePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ConsoleRect(ConsolePoint):
    def __init__(self, x, y, width, height):
        ConsolePoint.__init__(self, x, y)
        self.width = width
        self.height = height


def by_priority(layer):
    return layer.priority
