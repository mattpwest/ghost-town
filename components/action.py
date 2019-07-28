class Action:
    def __init__(self, name, cost):
        self.cost = cost
        self.name = name


class MoveAction(Action):
    def __init__(self, delta):
        Action.__init__(self, "Move", 1000)

        self.delta = delta


class PickupAction(Action):
    def __init__(self):
        Action.__init__(self, "Pick Up", 1000)


class DropAction(Action):
    def __init__(self, item):
        Action.__init__(self, "Drop", 1000)
        self.item = item


class NoAction(Action):
    def __init__(self):
        Action.__init__(self, "Nothing", 1000)


class QuitAction(Action):
    def __init__(self):
        Action.__init__(self, "Quit", 0)


class FullscreenAction(Action):
    def __init__(self):
        Action.__init__(self, "Fullscreen", 0)


class LookAction(Action):
    def __init__(self):
        Action.__init__(self, "Look", 0)


class InventoryAction(Action):
    def __init__(self):
        Action.__init__(self, "Inventory", 0)
