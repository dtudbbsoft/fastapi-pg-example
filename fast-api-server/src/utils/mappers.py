from typing import TypeVar, Callable

from src.api.utils.contracts import PaginationContract
from src.schemas import Pagination


TSourceEntity = TypeVar("TSourceEntity")
TDestinationEntity = TypeVar("TDestinationEntity")


def convert_to_entities(
    model: PaginationContract[TSourceEntity],
    entity_mapper: Callable[[TSourceEntity], TDestinationEntity],
) -> Pagination[TDestinationEntity]:
    return Pagination[TDestinationEntity](
        cursor=model.get("cursor"),
        count=model.get("count"),
        remaining=model.get("remaining"),
        results=[entity_mapper(entity) for entity in model.get("results")],
    )
