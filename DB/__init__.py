import sqlalchemy as db
from sqlalchemy.orm import declarative_base


engine = db.create_engine('sqlite:///test.db')
Base = declarative_base()
