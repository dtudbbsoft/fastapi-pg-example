from abc import abstractmethod
from typing import TypeVar, Generic


TModel = TypeVar("TModel")
TEntity = TypeVar("TEntity")


class IRepository(Generic[TModel, TEntity]):
    @abstractmethod
    async def upsert(self, externalId: str, entity: TEntity) -> None:
        pass
