from states import State


class GameState:
    def __init__(self, start_state=State.MENU):
        self.running = True
        self.state = None
        self.new_state = start_state

        self.menus = []
        self.new_game()
        self.menu_selected = 0

    def new_game(self):
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

    def resume_game(self):
        self.menus = [
            {
                "state": State.MAP,
                "text": "Resume"
            },
            {
                "state": State.QUIT,
                "text": "Quit Game"
            }
        ]
