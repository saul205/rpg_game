import sqlalchemy as db
from Repositories.Items import ItemRepository
from DB import Base


class ItemEntity(Base):
    __tablename__ = "item"
    __mapper_args__ = {'polymorphic_identity': 'item'}

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    name = db.Column(db.String, unique=True)
    level = db.Column(db.Integer)
    description = db.Column(db.String)
    amount = db.Column(db.Integer)

    @staticmethod
    def to_entity(item):
        item_entity = ItemEntity()
        item_entity.name = item.name
        item_entity.level = item.level
        item_entity.amount = item.clase
        item_entity.description = item.description

        return item_entity

    @staticmethod
    def from_entity(item_entity):
        item = ItemRepository.Item()
        item.level = item_entity.level
        item.name = item_entity.name
        item.amount = item.amount
        item.description = item_entity.description

        return item

    def __str__(self):
        return self.name + " - " + str(self.amount) + " - " + str(self.level) + ": " + self.description
