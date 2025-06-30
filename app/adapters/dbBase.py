# app/adapters/db_base.py

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Any
from sqlalchemy.orm import Session

T = TypeVar('T')

class DBAdapterBase(ABC, Generic[T]):
    @abstractmethod
    def create(self, db: Session, data: T) -> T:
        pass

    @abstractmethod
    def read(self, db: Session, query: dict) -> List[T]:
        pass

    @abstractmethod
    def update(self, db: Session, db_obj: T, new_data: T) -> T:
        pass

    @abstractmethod
    def delete(self, db: Session, obj_id: Any) -> bool:
        pass
