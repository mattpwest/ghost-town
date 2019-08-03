class Essence:
    def __init__(self, value, maximum=None):
        self.value = value

        if not maximum:
            self.maximum = value
        else:
            self.maximum = maximum
