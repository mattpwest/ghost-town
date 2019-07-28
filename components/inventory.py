class Inventory:
    def __init__(self, limit=5):
        self.limit = 5
        self.items = []
        self.selected = -1
        self.selected_action = -1
