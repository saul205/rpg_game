import Hero as h
from AttackRepository import *


class Archer(h.Hero):
    _baseHp = 100
    _baseMp = 100
    _baseDmg = 35
    _hpScalingFactor = 1.6
    _hpScalingFactor = 2

    _attacks = [
        Attack(),
        ChargedShot(),
        RapidFire()
    ]


class Mage(h.Hero):
    _baseHp = 100
    _baseMp = 150
    _baseDmg = 20
    _hpScalingFactor = 1.6
    _hpScalingFactor = 2

    _attacks = [
        Attack(),
        Fireball(),
        Thunder()
    ]


class Warrior(h.Hero):
    _baseHp = 150
    _baseMp = 50
    _baseDmg = 30
    _hpScalingFactor = 1.6
    _hpScalingFactor = 2

    _attacks = [
        Attack(),
        ShieldBash(),
        Stab()
    ]


classes = {
    "Archer": Archer,
    "Mage": Mage,
    "Warrior": Warrior
}
