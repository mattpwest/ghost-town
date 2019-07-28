from enum import Enum, auto


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


class OpenInventoryAction(Action):
    def __init__(self):
        Action.__init__(self, "Inventory", 0)


# Inventory actions are triggered from the player inventory and can target different things
class TargetType(Enum):
    SELF = auto()
    CREATURE = auto()


class InventoryAction(Action):
    def __init__(self, name, cost, item, target_type=TargetType.SELF):
        Action.__init__(self, name, cost)
        self.item = item
        self.target = None
        self.target_type = target_type


class DropAction(InventoryAction):
    def __init__(self, item):
        InventoryAction.__init__(self, "Drop", 1000, item)


class DrinkAction(InventoryAction):
    def __init__(self, item):
        InventoryAction.__init__(self, "Drink", 1000, item)
