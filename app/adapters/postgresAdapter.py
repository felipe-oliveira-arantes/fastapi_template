# app/adapters/postgres_adapter.py

from typing import Generic, TypeVar, Type, Optional, List, Any, Union
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, select

from app.adapters.dbBase import DBAdapterBase

T = TypeVar("T", bound=SQLModel)

class PostgreSQLAdapter(DBAdapterBase[T], Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, db: Session, obj_in: Union[T, dict]) -> T:
        if isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        else:
            db_obj = obj_in
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read(self, db: Session, query: dict = {}) -> List[T]:
        stmt = select(self.model)
        for attr, value in query.items():
            stmt = stmt.where(getattr(self.model, attr) == value)
        return db.exec(stmt).all()

    def update(self, db: Session, db_obj: T, obj_in: Union[T, dict]) -> T:
        obj_data = obj_in.dict(exclude_unset=True) if isinstance(obj_in, SQLModel) else obj_in
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, obj_id: Any) -> bool:
        obj = db.get(self.model, obj_id)
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True
