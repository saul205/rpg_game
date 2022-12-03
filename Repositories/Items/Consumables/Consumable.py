from Repositories.Items.Item import Item


class Consumable(Item):
    _healAmount = 0
    _manaAmount = 0

    def __init__(self):
        super().__init__()

        self.healAmount = self._healAmount
        self.manaAmount = self._manaAmount

    @property
    def empty(self):
        return self.amount <= 0

    def use(self, character):
        character.heal(self.healAmount)
        character.restore_mana(self.manaAmount)
        self.amount -= 1