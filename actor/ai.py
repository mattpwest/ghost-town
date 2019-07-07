import logging

from components import NoAction


class AIStrategy:
    def __init__(self):
        self.log = logging.getLogger("AIStrategy")
        self.log.setLevel(logging.INFO)

    def act(self):
        self.log.debug("AI is thinking...")
        return NoAction()
