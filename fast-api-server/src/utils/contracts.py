from typing import TypedDict, List, Generic, TypeVar

TEntity = TypeVar("TEntity")


class PaginationContract(TypedDict, Generic[TEntity]):
    cursor: int
    count: int
    remaining: int
    results: List[TEntity]
