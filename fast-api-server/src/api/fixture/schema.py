from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field, ConfigDict, model_validator, AnyUrl
from starlette import status

from src.api.commons.schemas import FilterQuery
from src.constants import EXTRA_FIELDS
from src.utils import PydanticModelMeta


class ExternalFixture(BaseModel):
    """External Fixture model"""

    id: Optional[str] = Field(None, alias="_id")
    modified_date: Optional[str] = Field(None, alias="Modified Date")
    created_date: Optional[str] = Field(None, alias="Created Date")
    created_by: Optional[str] = Field(None, alias="Created By")
    name: Optional[str] = Field(None, alias="Name")
    fixture_url: Optional[str] = Field(None, alias="Fixture url")
    demo: Optional[bool] = Field(None, alias="Demo")
    statuses: Optional[list[str]] = Field(None, alias="Statuses")

    model_config = ConfigDict(populate_by_name=True)


class Fixture(BaseModel):
    id: Optional[int] = None
    externalId: Optional[str] = None
    name: Optional[str] = None
    fixtureUrl: Optional[AnyUrl] = None
    demo: Optional[bool] = None
    flags: Optional[List[str]] = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class FixtureUpdate(Fixture, metaclass=PydanticModelMeta):
    __exclude_parent_fields__ = EXTRA_FIELDS


class FixtureCreate(Fixture, metaclass=PydanticModelMeta):
    __exclude_parent_fields__ = EXTRA_FIELDS

    name: str = Field(..., min_length=1)

    @model_validator(mode="after")
    def required_fields(self):
        required_fields = [
            ("fixtureUrl", self.fixtureUrl),
        ]
        for field_name, field_value in required_fields:
            if not field_value:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"{field_name} is required.",
                )

        return self



class FixtureSearchQuery(FilterQuery, BaseModel):
    company_id: Optional[str] = Field(None, alias="companyId")
    synchronize: bool = Field(False, alias="synchronize")
