import random as rand

import Effects as Ef
from AttackRepository import Attack


class Character:
    _baseHp = 100
    _baseMp = 100
    _attacks = [Attack()]
    _baseDmg = 20
    _hpScalingFactor = 1.6
    _name = 'Character'

    @property
    def _hp_scaling(self):
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
    def print_hp(self):
        print(self.hp)

    # endregion

    # region Formulas
    def _hp_formula(self):
        return int(self._baseHp + (self.level ** self._hp_scaling / self._hp_scaling) + self._baseHp * self.level / 10)

    def _dmg_formula(self):
        return int(self._baseDmg * self.level)

    # endregion

    # region Character State

    def has_mana(self, mana_cost):
        return self.mp >= mana_cost

    def die(self):
        if self.hp > 0:
            return

        print("I died", self.hp)
        self.dead = True

    def reset(self):

        self.tempDR = [(x, y - 1) for x, y in self.tempDR if y > 1]
        self.defending = False
        self.manaRegen = True

    def check_invariants(self):

        if self.mp > self.maxMp:
            self.mp = self.maxMp

        if self.hp > self.maxHp:
            self.hp = self.maxHp

    # endregion

    # region Combate
    def launch_attack(self, target, attack):

        hit = target.get_attacked(self, attack)

        if attack.costs_mana:
            self.consume_mana(attack.manaCost)

    def get_attacked(self, attacker, attack_action):
        # Acciones pre-hit

        # Comprobar golpeo
        if not attack_action.did_hit():
            return False

        # Golpeo
        amount = int(attack_action.dmgMultiplier *
                     attacker.dmg)
        self.lower_hp_dr(amount)

        # After-hit
        self.proc_effects(attack_action.effects)
        return True

    def defend(self):

        self.defending = True
        self.tempDR.append((.5, 1))

    # endregion

    # region Efectos
    def proc_effects(self, effects):

        for effect in effects:

            roll = rand.uniform(0, 1)
            if roll <= effect.chance:
                self.states[effect.state] = effect

    def apply_effects(self):

        effect_applied = False
        for effect in self.states:
            effect_applied = True
            self.states[effect].apply(self)

        return effect_applied

    @property
    def stunned(self):
        if Ef.Effects.Stun in self.states:
            self.states[Ef.Effects.Stun].duration -= 1
            self.states[Ef.Effects.Stun].print_msg()
            return True

        return False

    # endregion

    # region HP management
    def _lower_hp(self, amount):

        self.hp -= amount
        self.die()

    def lower_hp_dr(self, amount):

        dr = 1 - (sum([x for x, y in self.tempDR]) + self.DR)
        self._lower_hp(amount * dr if dr >= 0 else 0)

    def lower_hp_status(self, dmg, perc_dmg):

        damage = dmg
        if perc_dmg:
            damage = self.hp * perc_dmg

        self._lower_hp(damage)

    def heal(self, amount):

        self.hp += amount
        self.check_invariants()

    # endregion

    # region MP management

    def restore_mana(self, amount):

        self.mp += amount
        self.check_invariants()

    def consume_mana(self, amount):
        self.mp -= amount
        self.manaRegen = False

    # endregion
