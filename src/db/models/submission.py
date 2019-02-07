from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import INTEGER, String, TEXT

from .base import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(INTEGER, primary_key=True)
    reddit_id = Column(String(32), unique=True, nullable=False)
    title = Column(TEXT, nullable=False)
    text = Column(TEXT)
    permalink = Column(TEXT)
    url = Column(TEXT)
    author_id = Column(INTEGER, ForeignKey("users.id"), nullable=False)
    subreddit_id = Column(INTEGER, ForeignKey("subreddits.id"), nullable=False)
