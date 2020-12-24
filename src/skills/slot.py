class Slot:

    def __init__(self, id: str, name: str, aliases, pattern: str = None):
        self.id = id
        self.name = name
        self.aliases = aliases
        self.pattern = pattern