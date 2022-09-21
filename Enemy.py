from Character import *
from ItemRepository import Potion


class Enemy(Character):

    _baseExp = 20
    _expScaling = 2.5
    _expLevelDiffScaling = 1.2
    _heroes = []
    _hpScalingFactor = 2.5
    _baseDmg = 5
    _name = "Enemy"
    _drops = [Potion()]

    def __init__(self, level):
        super().__init__()
        self.level = level
        self.maxHp = self._hpFormula()
        self.hp = self.maxHp
        self.dmg = self._dmgFormula()

    def _expFormula(self, heroLvl):
        return int(self._baseExp + ((self.level-1)**self._expLevelDiffScaling/heroLvl) ** self._expScaling)

    def _dmgFormula(self):
        return self._baseDmg * self.level + self.level ** 2.3 / self._baseDmg ** 2

    def __str__(self):
        result = "--------------------------------------" + \
            "\n" + self._name + " Lvl " + str(self.level) + \
            "\nHP " + str(self.hp) + "/" + str(self.maxHp) + \
            "\n--------------------------------------"
        return result

    def expGiven(self, heroLvl):
        return self._expFormula(heroLvl)

    def drop(self):

        return self._drops
