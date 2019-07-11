import logging

from components import NoAction, Text, Viewable


class AIStrategy:
    def __init__(self):
        self.log = logging.getLogger("AIStrategy")
        self.log.setLevel(logging.INFO)

    def act(self, entity, world):
        text = world.component_for_entity(entity, Text)
        viewable = world.component_for_entity(entity, Viewable)

        if viewable.lit:
            self.log.info("The " + text.noun + " wonders when it will get a turn?!")

        return NoAction()
