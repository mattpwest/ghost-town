import tcod as libtcod


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color
        self.age = 0


class MessageLog:
    def __init__(self, limit=100):
        self.limit = limit
        self.log = []

    def add(self, text, color=libtcod.white):
        self.add_message(Message(text, color))

    def add_message(self, message):
        self.log.append(message)

        if len(self.log) > self.limit:
            del self.log[0]
