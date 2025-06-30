# app/dependencies/container.py
from sqlmodel import Session as SQLSession, create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql://clinic:123456@localhost:5432/clinic_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=SQLSession, autocommit=False, autoflush=False)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
