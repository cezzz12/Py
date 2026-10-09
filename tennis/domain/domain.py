class Player:
    def __init__(self, id, name, strength):
        self.name = name
        self.id=id
        self.strength = strength

    def __str__(self):
        return f"{self.id},{self.name},{self.strength}"

    def increase_strength(self):
        self.strength += 1