from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.schemas import SortMixin, FilterOperator

class FilterQuery(SortMixin, BaseModel):
    limit: int = Field(10, ge=1, description="The number of results to return")
    offset: int = Field(0, ge=0, description="The starting point for the results")
    filter_value: Optional[str] = Field(
        None,
        description="The value to use for filtering",
    )
    filter_operator: Optional[str] = Field(
        None,
        description="The operator to use for filtering",
        examples=list(FilterOperator),
    )
    filter_field: Optional[str] = Field(
        None,
        description="Field for filtering",
        examples=["name"],
    )
    search_term: str = Field("", description="Search term")

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)