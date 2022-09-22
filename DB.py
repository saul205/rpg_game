import sqlalchemy as db
from sqlalchemy.orm import Session, declarative_base

import Classes as c

engine = db.create_engine('sqlite:///test.db')
Base = declarative_base()


class PlayerEntity(Base):
    __tablename__ = "player"

    name = db.Column(db.String, primary_key=True)
    exp = db.Column(db.Integer)
    level = db.Column(db.Integer)
    clase = db.Column(db.String)

    @staticmethod
    def to_entity(player):
        player_entity = PlayerEntity()
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


class PlayerController:

    @staticmethod
    def get_all_players():

        with Session(engine) as session:

            try:
                players = session.query(PlayerEntity).all()
                return players
            except Exception:
                session.rollback()
                raise

    @staticmethod
    def save_player(player):

        with Session(engine) as session:
            player_entity = PlayerEntity.to_entity(player)
            try:
                session.add(player_entity)
            except Exception:
                session.rollback()
                raise
            else:
                session.commit()

    @staticmethod
    def update_player(player):

        with Session(engine) as session:
            try:
                player_entity = session.query(
                    PlayerEntity).filter_by(name=player.name).first()
                player_entity.level = player.level
                player_entity.exp = player.exp
            except Exception:
                session.rollback()
                raise
            else:
                session.commit()

    @staticmethod
    def delete_player(player_name):

        with Session(engine) as session:
            try:
                player_entity = session.query(
                    PlayerEntity).filter_by(name=player_name).first()
                session.delete(player_entity)
            except Exception:
                session.rollback()
                raise
            else:
                session.commit()


Base.metadata.create_all(engine)

'''import Classes as c



with Session(engine) as session:

    archer = session.query(PlayerEntity).filter_by(name="kl4ws").first()
    archer2 = c.classes[archer.clase](archer.name)

    print(archer2)
    archer2.exp = archer.exp
    archer2.add_exp(5000)
    print(archer2)


    archer.name = archer2.name
    archer.exp = archer2.exp
    archer.clase = archer2.clase

    session.commit()

    for pe in session.query(PlayerEntity).all():
        print(pe.name, pe.exp, pe.clase)

        a = c.classes[pe.clase](pe.name)
        a.add_exp(pe.exp)

        print(a)'''
