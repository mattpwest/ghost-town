class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False
        
        if block_sight is None:
            self.block_sight = blocked
        else:
            self.block_sight = block_sight
    