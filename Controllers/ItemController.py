from DB.Entities.ItemEntity import ItemEntity
from sqlalchemy.orm import Session
from DB import engine


class ItemController:

    @staticmethod
    def get_all():

        with Session(engine) as session:
            try:
                items = session.query(ItemEntity).all()
                return items
            except Exception:
                session.rollback()
                raise

    @staticmethod
    def save_items(items, session=None):

        if session is None:
            session = Session(engine)

        try:
            session.add_all([ItemEntity.to_entity(item) for item in items])
        except Exception:
            session.rollback()
            raise
        else:
            session.commit()


    @staticmethod
    def get_items(player_id, session=None):

        if session is None:
            session = Session(engine)

        try:
            session.query(ItemEntity).where(ItemEntity.player == player_id)
        except Exception:
            session.rollback()
            raise



