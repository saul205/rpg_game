from DB.Entities.PlayerEntity import PlayerEntity
from sqlalchemy.orm import Session
from DB import engine
from Controllers.ItemController import ItemController as ic


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
    def get_all_names():

        with Session(engine) as session:
            try:
                names = session.query(PlayerEntity).filter_by(PlayerEntity.name).all()
                return names
            except Exception:
                session.rollback()
                raise

    @staticmethod
    def save_player(player):

        with Session(engine) as session:
            try:
                player_entity = PlayerEntity.to_entity(player)
                session.add(player_entity)
                session.flush()
                session.refresh(player_entity)
                ic.save_items(player_entity.id)
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
