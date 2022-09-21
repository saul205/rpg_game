
class Item():

    name = ''
    descripcion = ''

    def __init__(self):

        self.nivel = 0

    def use(self, character):

        return

    def __str__(self):

        return self.name + ": " + self.descripcion

# region Consumibles


class Consumible(Item):

    _healAmount = 0
    _manaAmount = 0

    def __init__(self):

        super().__init__()

        self.healAmount = self._healAmount
        self.manaAmount = self._manaAmount

        self.consumed = False

    def use(self, character):

        character.heal(self.healAmount)
        character.restoreMana(self.manaAmount)


class Potion(Consumible):

    _healAmount = 20
    name = 'Pocion'
    descripcion = 'Cura 20 ps'

# endregion
