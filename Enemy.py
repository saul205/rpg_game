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
        self.maxHp = self._hp_formula()
        self.hp = self.maxHp
        self.dmg = self._dmg_formula()

    def _exp_formula(self, heroLvl):
        return int(self._baseExp + ((self.level - 1) ** self._expLevelDiffScaling / heroLvl) ** self._expScaling)

    def _dmg_formula(self):
        return self._baseDmg * self.level + self.level ** 2.3 / self._baseDmg ** 2

    def __str__(self):
        result = "--------------------------------------" + \
                 "\n" + self._name + " Lvl " + str(self.level) + \
                 "\nHP " + str(self.hp) + "/" + str(self.maxHp) + \
                 "\n--------------------------------------"
        return result

    def exp_given(self, hero_lvl):
        return self._exp_formula(hero_lvl)

    def drop(self):
        return self._drops
