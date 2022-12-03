import sqlalchemy as db
from sqlalchemy.orm import relationship
import Classes as c
from DB import Base


class PlayerEntity(Base):
    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    exp = db.Column(db.Integer)
    level = db.Column(db.Integer)
    clase = db.Column(db.String)
    inventory = relationship("ItemEntity")

    @staticmethod
    def to_entity(player):
        player_entity = PlayerEntity()
        player_entity.id = player.id
        player_entity.name = player.name
        player_entity.exp = player.exp
        player_entity.level = player.level
        player_entity.clase = player.clase

        return player_entity

    @staticmethod
    def from_entity(player_entity):
        player = c.classes[player_entity.clase](player_entity.name)
        player.add_exp_number(player_entity.exp)

        return player

    def __str__(self):
        return self.name + " - " + self.clase + " - " + str(self.level)