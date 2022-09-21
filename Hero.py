from Character import *


class Hero(Character):

    _expToLevel = 120
    _expFactor = 2
    _hpScalingFactor = 2
    _dmScaling = 0.25

    def __init__(self, name):
        super().__init__()
        self.exp = 0
        self.expToLevel = 120
        self._clase = self.__class__.__name__
        self.name = name

        # Initialize Inventory
        self.inventory = {}

    def __str__(self):
        result = "--------------------------------------" + \
            "\n" + self.name + " - " + self._clase + \
            "\nHP " + str(self.hp) + "/" + str(self.maxHp) + \
            "\nMP " + str(self.mp) + \
            "\nLvl " + str(self.level) + ' Exp ' + str(self.exp) + '/' + str(self.expToLevel) + \
            "\n--------------------------------------"
        return result

    # region Exp management

    def levelUp(self):
        leveled = False
        while self.exp >= self.expToLevel:
            print(self.exp, self.expToLevel)
            self.level += 1
            leveled = True
            self.expToLevel = int(2 * (self._expToLevel * (self.level-1)) +
                                  (self._expFactor**(self.level-1) + 1)/(self._expFactor - 1))

        if leveled:
            self.maxHp = self._hpFormula()
            self.hp = self.maxHp
            self.dmg = self._dmgFormula()

    def addExp(self, enemy):
        self.addExpNumber(enemy.expGiven(self.level))

        self.levelUp()

    def addExpNumber(self, exp):

        self.exp += exp

        self.levelUp()

    # endregion

    # region Attacks

    def selectAttack(self, ataque):

        return self.attacks[int(ataque) - 1]

    def printAttacks(self):
        result = "Ataques: "
        for x in self.attacks:
            result += '\n\t->' + x.name + "- Dmg: " + \
                str(x.dmgMultiplier * self.dmg) + \
                " | Hit Chance: " + str(x.hitChance*100) + "%"

        print(result)

    # endregion

    # region Mana Management

    def regenerateMana(self):

        if self.manaRegen:
            mana = rand.randint(2, 10)
            self.restoreMana(20 if self.defending else mana)

    # endregion

    # region Inventory

    def printInventory(self):

        result = "Inventory:"
        for item in self.inventory:

            result += "\n\t-> " + str(self.inventory[item][1]) + " " +\
                str(self.inventory[item][0])

        print(result)

    def addToInventory(self, items):

        for item in items:
            if item.name in self.inventory:
                self.inventory[item.name][1] += 1
            else:
                self.inventory[item.name] = [item, 1]

    # endregion

    # region Formule Overload

    def _dmgFormula(self):
        return int(self._baseDmg + (self.level*(self.level-1))/50 + self._dmScaling*self._baseDmg*self.level)

    # endregion
