class Item:
    name = ''
    description = ''

    def __init__(self):
        self.level = 0
        self.amount = 1

    def use(self, character):
        return

    def __str__(self):
        return self.name + ": " + self.description
