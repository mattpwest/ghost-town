class Essence:
    def __init__(self, value, maximum=None):
        self.value = value

        if not maximum:
            self.maximum = value
        else:
            self.maximum = maximum


class EssenceAbsorber:
    def __init__(self, range=1, strength=10, frequency=1000):
        self.range = range
        self.strength = strength
        self.frequency = frequency
        self.time_passed = 0
