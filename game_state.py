from states import State


class GameState:
    def __init__(self, start_state=State.MAP):
        self.running = True
        self.state = None
        self.new_state = start_state
