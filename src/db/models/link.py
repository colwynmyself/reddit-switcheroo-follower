from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import INTEGER, String

from .base import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(INTEGER, primary_key=True)
    url = Column(String(500), nullable=False)
    text = Column(String(100), nullable=False)
    depth = Column(INTEGER, nullable=False)
    parent_link_id = Column(INTEGER, ForeignKey("links.id"))
