class Possessor:
    def __init__(self, cost_multiplier=1.0):
        self.cost_multiplier = cost_multiplier
        self.my_components = []
        self.target_components = []


class Possession:
    def __init__(self, from_entity):
        self.from_entity = from_entity
