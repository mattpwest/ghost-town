class Health:
    def __init__(self, points, maximum=None):
        self.points = points

        if maximum is not None and maximum >= points:
            self.maximum = maximum
        else:
            self.maximum = points
