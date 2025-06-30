from typing import TypeVar, Generic, Type, List, Optional

from app.adapters.dbBase import DBAdapterBase
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseBO(Generic[T]):
    def __init__(
        self,
        db_adapter: DBAdapterBase[T],
        model_type: Type[T]
    ):
        self.db_adapter = db_adapter
        self.model_type = model_type

    def create(self, data: T) -> Optional[T]:
        return self.db_adapter.create(self.model_type.__name__.lower() + "s", data)
    
    def read(self, query: dict) -> List[T]:
        return self.db_adapter.read(self.model_type.__name__.lower() + "s", query)

    def update(self, query: dict, new_data: T) -> bool:
        return self.db_adapter.update(self.model_type.__name__.lower() + "s", query, new_data)

    def delete(self, query: dict) -> bool:
        return self.db_adapter.delete(self.model_type.__name__.lower() + "s", query)
