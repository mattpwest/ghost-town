class Text:
    def __init__(self, noun, pronoun=None, description=None):
        self.noun = noun

        if pronoun is not None:
            self.pronoun = pronoun
        else:
            self.pronoun = self.noun.capitalize()

        if description is not None:
            self.description = description
        else:
            self.description = 'No description...'
