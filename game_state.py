from states import State


class GameState:
    def __init__(self, start_state=State.MENU):
        self.running = True
        self.state = None
        self.new_state = start_state

        self.menus = [
            {
                "state": State.GENERATE,
                "text": "New Game"
            },
            {
                "state": State.QUIT,
                "text": "Quit Game"
            }
        ]
        self.menu_selected = 0
