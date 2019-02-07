from sqlalchemy import Table, Column
from sqlalchemy.types import INTEGER, String

from .base import Base


class Subreddit(Base):
    __tablename__ = "subreddits"

    id = Column(INTEGER, primary_key=True)
    reddit_id = Column(String(32), unique=True, nullable=False)
    name = Column(String(32), nullable=False)
