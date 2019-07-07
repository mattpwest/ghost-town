class Actor:
    def __init__(self, strategy, gain=500, cost=1000, initial=0):
        self.strategy = strategy
        self.energy = initial
        self.gain = gain
        self.cost = cost
