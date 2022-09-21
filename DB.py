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
    def ToEntity(player):

        playerEntity = PlayerEntity()
        playerEntity.name = player.name
        playerEntity.exp = player.exp
        playerEntity.level = player.level
        playerEntity.clase = player._clase

        return playerEntity

    @staticmethod
    def FromEntity(playerEntity):

        player = c.classes[playerEntity.clase](playerEntity.name)
        player.addExpNumber(playerEntity.exp)

        return player

    def __str__(self):

        return self.name + " - " + self.clase + " - " + str(self.level)


class PlayerController():

    @staticmethod
    def getAllPlayers():

        with Session(engine) as session:

            try:
                players = session.query(PlayerEntity).all()
                return players
            except:
                session.rollback()
                raise

    @staticmethod
    def savePlayer(player):

        with Session(engine) as session:
            playerEntity = PlayerEntity.ToEntity(player)
            try:
                session.add(playerEntity)
            except:
                session.rollback()
                raise
            else:
                session.commit()

    @staticmethod
    def updatePlayer(player):

        with Session(engine) as session:
            try:
                playerEntity = session.query(
                    PlayerEntity).filter_by(name=player.name).first()
                playerEntity.level = player.level
                playerEntity.exp = player.exp
            except:
                session.rollback()
                raise
            else:
                session.commit()

    @staticmethod
    def deletePlayer(playerName):

        with Session(engine) as session:
            try:
                playerEntity = session.query(
                    PlayerEntity).filter_by(name=playerName).first()
                session.delete(playerEntity)
            except:
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
    archer2.addExp(5000)
    print(archer2)


    archer.name = archer2.name
    archer.exp = archer2.exp
    archer.clase = archer2._clase

    session.commit()

    for pe in session.query(PlayerEntity).all():
        print(pe.name, pe.exp, pe.clase)

        a = c.classes[pe.clase](pe.name)
        a.addExp(pe.exp)

        print(a)'''
