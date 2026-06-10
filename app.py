from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base


db_url = "sqlite:///database.db"

engine = create_engine(db_url)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(type_=Integer, primary_key=True, autoincrement="auto")
    name = Column(type_=String)
    age = Column(type_=Integer)


Base.metadata.create_all(engine)