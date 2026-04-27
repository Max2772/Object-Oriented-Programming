from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from LB7.src.shared.config import settings
from LB7.src.models.entities import Base

engine = create_engine(
    settings.DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
