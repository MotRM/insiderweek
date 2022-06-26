import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_dir = os.path.abspath(os.path.dirname(__file__))

Base = declarative_base()

engine = create_engine(
    "sqlite:///" + os.path.join(db_dir, "db.sqlite"),
    connect_args={"check_same_thread": False},
    echo=True,
)

Session = sessionmaker(bind=engine)
session = Session()
