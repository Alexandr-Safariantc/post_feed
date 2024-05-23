from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """Change db for tests and for deploy."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
