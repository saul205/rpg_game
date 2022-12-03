import sqlalchemy as db
from Repositories.Items.Consumables import ConsumableRepository as cr
from DB.Entities.ItemEntity import ItemEntity


class ConsumableEntity(ItemEntity):
    __tablename__ = "consumable"
    id = db.Column(db.Integer, db.ForeignKey("item.id"), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'consumable'}

    @staticmethod
    def to_entity(consumable):
        consumable_entity = ConsumableEntity()
        consumable_entity.name = consumable.name
        consumable_entity.level = consumable.level
        consumable_entity.amount = consumable.clase
        consumable_entity.description = consumable.description

        return consumable_entity

    @staticmethod
    def from_entity(consumable_entity):
        consumable = cr[consumable_entity.name]()
        consumable.level = consumable_entity.level
        consumable.name = consumable_entity.name
        consumable.amount = consumable.amount
        consumable.description = consumable_entity.description

        return consumable

    def __str__(self):
        return self.name + " - " + str(self.amount) + " - " + str(self.level) + ": " + self.description
