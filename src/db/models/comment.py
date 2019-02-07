from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import INTEGER, DateTime, TEXT, Boolean, String

from .base import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(INTEGER, primary_key=True)
    reddit_id = Column(String(32), unique=True, nullable=False)
    body = Column(TEXT)
    permalink = Column(TEXT)
    submission_id = Column(INTEGER, ForeignKey("submissions.id"))
    author_id = Column(INTEGER, ForeignKey("users.id"), nullable=False)
    parent_comment_id = Column(INTEGER, ForeignKey("comments.id"))
    subreddit_id = Column(INTEGER, ForeignKey("subreddits.id"), nullable=False)
