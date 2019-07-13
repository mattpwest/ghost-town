class RenderState:
    def __init__(self):
        self.consoles = ConsolesState


class ConsolesState:
    def __init__(self):
        self.root = None
        self.map = None
        self.ui = None
