import random as rand
from AttackRepository import Attack
import numpy as np
import Effects as ef


class Character:

    _baseHp = 100
    _baseMp = 100
    _attacks = [Attack()]
    _baseDmg = 20
    _hpScalingFactor = 1.6
    _name = 'Character'

    @property
    def _hpScaling(self):
        return self._baseHp / 100 * self._hpScalingFactor

    def __init__(self):
        # Miembros de instancia
        self.level = 1
        self.hp = self._baseHp
        self.maxHp = self._baseHp
        self.mp = self._baseMp
        self.maxMp = self._baseMp
        self.attacks = self._attacks
        self.dmg = self._baseDmg
        self.dead = False
        self.states = {}
        self.name = self._name

        self.manaRegen = True
        self.defending = False

        # Damage Reductions
        self.DR = 0
        self.tempDR = []

    # region Prints
    def printHp(self):
        print(self.hp)
    # endregion

    # region Formulas
    def _hpFormula(self):
        return int(self._baseHp + (self.level ** self._hpScaling/self._hpScaling) + self._baseHp*self.level / 10)

    def _dmgFormula(self):
        return int(self._baseDmg * self.level)
    # endregion

    # region Character State

    def hasMana(self, manaCost):
        return self.mp >= manaCost

    def die(self):
        if self.hp > 0:
            return

        print("I died", self.hp)
        self.dead = True

    def reset(self):

        self.tempDR = [(x, y-1) for x, y in self.tempDR if y > 1]
        self.defending = False
        self.manaRegen = True

    def checkInvariants(self):

        if self.mp > self.maxMp:
            self.mp = self.maxMp

        if self.hp > self.maxHp:
            self.hp = self.maxHp

    # endregion

    # region Combate
    def launchAttack(self, target, attack):

        hit = target.getAttacked(self, attack)

        if attack.costsMana:
            self.consumeMana(attack.manaCost)

    def getAttacked(self, attacker, attackAction):
        # Acciones pre-hit

        # Comprobar golpeo
        if not attackAction.didHit():
            return False

        # Golpeo
        amount = int(attackAction.dmgMultiplier *
                     attacker.dmg)
        self.lowerHpDR(amount)

        # After-hit
        self.procEffects(attackAction.effects)
        return True

    def defend(self):

        self.defending = True
        self.tempDR.append((.5, 1))
    # endregion

    # region Efectos
    def procEffects(self, effects):

        for effect in effects:

            roll = rand.uniform(0, 1)
            if roll <= effect.chance:

                self.states[effect.state] = effect

    def applyEffects(self):

        effectApplied = False
        for effect in self.states:
            effectApplied = True
            self.states[effect].apply(self)

        return effectApplied

    @property
    def Stunned(self):
        if ef.Effects.Stun in self.states:

            self.states[ef.Effects.Stun].duration -= 1
            self.states[ef.Effects.Stun].printMsg()
            return True

        return False
    # endregion

    # region HP management
    def __lowerHp(self, amount):

        self.hp -= amount
        self.die()

    def lowerHpDR(self, amount):

        dr = 1 - (sum([x for x, y in self.tempDR]) + self.DR)
        self.__lowerHp(amount * dr if dr >= 0 else 0)

    def lowerHpStatus(self, dmg, percDmg):

        damage = dmg
        if percDmg:
            damage = self.hp * percDmg

        self.__lowerHp(damage)

    def heal(self, amount):

        self.hp += amount
        self.checkInvariants()
    # endregion

    # region MP management

    def restoreMana(self, amount):

        self.mp += amount
        self.checkInvariants()

    def consumeMana(self, amount):
        self.mp -= amount
        self.manaRegen = False

    # endregion
