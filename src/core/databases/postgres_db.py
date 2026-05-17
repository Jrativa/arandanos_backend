# src/core/databases/postgres_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializa la base de datos específica para Postgres."""
    from src.features.auth.infrastructure.postgres import models
     
    Base.metadata.create_all(bind=engine)