from sqlalchemy import Table, Column
from sqlalchemy.types import INTEGER, TEXT, String

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True)
    reddit_id = Column(String(32), unique=True, nullable=False)
    username = Column(TEXT, nullable=False)
