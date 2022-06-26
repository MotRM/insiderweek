# models.py

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))


class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    name = Column(String)
    order_date = Column(DateTime)
    price_1 = Column(Float)
    price_2 = Column(Float)
    price_3 = Column(Float)
    price_4 = Column(Float)
    user_id = Column(Integer, ForeignKey("user.id"))
