from sqlalchemy import Table, Column
from sqlalchemy.types import INTEGER, String

from src.models.db import Base


class Link(Base):
    __tablename__ = 'links'

    id = Column(INTEGER, primary_key=True)
    url = Column(String(500), nullable=False)
    text = Column(String(100), nullable=False)
    depth = Column(INTEGER, nullable=False)
