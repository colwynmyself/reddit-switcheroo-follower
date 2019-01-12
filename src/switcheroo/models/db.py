from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from src.switcheroo.config import config


def _generate_connection_string():
    return 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        config.db_user,
        config.db_pass,
        config.db_host,
        config.db_port,
        config.db_name,
    )


class Db:

    def __init__(self):
        self._engine = create_engine(
            _generate_connection_string(), pool_pre_ping=True)
        self._sessionmaker = sessionmaker(bind=self._engine, autoflush=True)

    def create_session(self):
        return self._sessionmaker()


Base = declarative_base()
