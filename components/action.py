class Action:
    def __init__(self, cost):
        self.cost = cost


class MoveAction(Action):
    def __init__(self, delta):
        Action.__init__(self, 1000)

        self.delta = delta


class PickupAction(Action):
    def __init__(self):
        Action.__init__(self, 1000)


class NoAction(Action):
    def __init__(self):
        Action.__init__(self, 1000)


class QuitAction(Action):
    def __init__(self):
        Action.__init__(self, 0)


class FullscreenAction(Action):
    def __init__(self):
        Action.__init__(self, 0)


class LookAction(Action):
    def __init__(self):
        Action.__init__(self, 0)
