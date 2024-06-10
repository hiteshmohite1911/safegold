from config.settings import get_settings
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine


settings = get_settings()

engine = create_engine(settings.DATABASE_URI)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
