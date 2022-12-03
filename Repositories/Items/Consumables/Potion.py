import Repositories.Items.Consumables.Consumable as c


class Potion(c.Consumable):
    _healAmount = 20
    name = 'Pocion'
    description = 'Cura 20 ps'