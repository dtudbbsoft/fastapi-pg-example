from enum import Enum, StrEnum
from typing import Generic, List, TypeVar, Optional
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import desc, asc

T = TypeVar("T")


class FilterOperator(str, Enum):
    CONTAINS = "contains"
    STARTS_WITH = "startsWith"
    IS_EMPTY = "isEmpty"
    IS_NOT_EMPTY = "isNotEmpty"
    EQUALS = "equals"
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_THAN_OR_EQUALS = ">="
    LESS_THAN_OR_EQUALS = "<="


class Pagination(BaseModel, Generic[T]):
    cursor: int = Field(..., ge=0)
    count: int = Field(..., ge=0)
    remaining: int = Field(..., ge=0)
    results: List[T]


class Id(BaseModel):
    id: int


class AcknowledgeMessage(BaseModel):
    message: str = "Success"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class SortMixin:
    sort_by: str = Field("id", alias="sortBy", description="Sort by", examples=["name"])
    sort_order: SortOrder = Field(
        "asc",
        alias="sortOrder",
        description="Sort order",
        examples=[SortOrder.DESC],
    )

    model_config = ConfigDict(populate_by_name=True)

    @property
    def sort_order_sql(self):
        return asc if self.sort_order == SortOrder.ASC else desc


class DAOGetAllParams(SortMixin, BaseModel):
    limit: int = 10
    offset: int = 0
    filter_field: Optional[str] = None
    filter_operator: Optional[str] = None
    filter_value: Optional[str] = None
    search_term: Optional[str] = None

    def apply_filter(self) -> bool:
        return all([self.filter_field, self.filter_operator, self.filter_value])


class IdName(BaseModel):
    id: int
    name: str
