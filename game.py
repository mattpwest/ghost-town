from states import State


class Game:
    def __init__(self, config, factory, messages, game_map, consoles, start_state=State.MAP):
        self.config = config
        self.factory = factory
        self.messages = messages
        self.map = game_map
        self.consoles = consoles

        self.running = True
        self.state = None
        self.new_state = start_state
