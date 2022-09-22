import enum


class Effects(enum.Enum):
    Poison = 0,
    Bleed = 1,
    Stun = 2
    Burn = 3


class Effect:
    _duration = 1
    _damage = 10
    _damagePerc = 0.05
    _chance = 0.1
    _msg = ""
    percDmg = False
    state = None

    def __init__(self):
        self.duration = self._duration
        self.damage = self._damage
        self.damagePerc = self._damagePerc
        self.chance = self._chance

    def apply(self):
        return

    def print_msg(self):
        print(self._msg)


class Stun(Effect):
    _msg = "You are stunned"
    state = Effects.Stun

    def __init__(self, duration, chance):
        super().__init__()

        self.duration = duration
        self.chance = chance


class Burn(Effect):
    _msg = "Recieve burn dmg"
    percDmg = False
    state = Effects.Burn

    def __init__(self, duration, chance, dmg):
        super().__init__()

        self.duration = duration
        self.chance = chance
        self.damage = dmg
        self._msg = self._msg + ": " + str(dmg)

    def apply(self, character):
        self.print_msg()
        character.lowerHpStatus(self.damage, self.percDmg)
