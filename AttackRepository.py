import random as rand

import Effects as Ef


class Attack:
    hitChance = 0.9
    dmgMultiplier = 1
    delay = 0
    manaCost = 0
    effects = []
    name = 'Default Attack'

    def did_hit(self):
        return rand.uniform(0, 1) <= self.hitChance

    @property
    def costs_mana(self):
        return self.manaCost > 0


class Status(Attack):
    hitChance = 1


# region MAGE


class Fireball(Attack):
    hitChance = 0.9
    dmgMultiplier = 2
    manaCost = 25
    effects = [
        Ef.Burn(2, 1, 10)
    ]
    name = 'Fireball'


class Thunder(Attack):
    hitChance = 0.9
    dmgMultiplier = 3.5
    manaCost = 65
    name = 'Thunder'


# endregion

# region ARCHER


class ChargedShot(Attack):
    hitChance = 0.9
    dmgMultiplier = 1.8
    manaCost = 45
    name = 'Charged Shot'


class RapidFire(Attack):
    hitChance = 0.9
    dmgMultiplier = 1.45
    manaCost = 25
    name = 'Rapid Fire'


# endregion

# region WARRIOR


class ShieldBash(Attack):
    hitChance = 0.9
    dmgMultiplier = 1.25
    manaCost = 10
    effects = [
        ef.Stun(2, 0.15)
    ]
    name = 'Shield Bash'


class Stab(Attack):
    hitChance = 0.9
    dmgMultiplier = 1.75
    manaCost = 30
    name = 'Stab'

# endregion
