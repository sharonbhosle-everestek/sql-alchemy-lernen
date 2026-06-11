from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine

DB_url = "sqlite:///database.db"

engine = create_engine(DB_url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# class BaseModel(Base):
#     __abstract__ = True
#     __allow_unmapped__ = True

class User(Base):
    __tablename__ = "user"

    user_id = Column(type_=Integer, primary_key=True)
    name = Column(type_=String)
    age = Column(type_=Integer)
    address = relationship("Address", back_populates="user", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "address"

    add_id = Column(type_=Integer, primary_key=True)
    user_id = Column(ForeignKey("user.user_id", ondelete="CASCADE"), type_=Integer, nullable=False)
    country = Column(type_=String)
    place = Column(type_=String)
    user = relationship("User", back_populates="address")


Base.metadata.create_all(engine)


