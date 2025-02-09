# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from app.db.base_class import Base  # Importa o mesmo Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./clients.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)