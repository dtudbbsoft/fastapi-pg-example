from typing import Annotated

from fastapi import APIRouter, Depends, Query
from starlette import status

from src.schemas import Pagination, AcknowledgeMessage, Id
from src.api.fixture.schema import Fixture, FixtureUpdate, FixtureCreate, FixtureSearchQuery
from src.api.fixture.service import FixtureService, get_fixture_service

router = APIRouter()


@router.get("", response_model=Pagination[Fixture], status_code=status.HTTP_200_OK)
async def get_fixtures(
    fixture_service: Annotated[FixtureService, Depends(get_fixture_service)],
    filters: Annotated[FixtureSearchQuery, Query()],
) -> Pagination[Fixture]:
    try:
        return await fixture_service.get_fixtures(filters)
    except Exception as e:
        import traceback
        traceback.print_tb(e.__traceback__)
        raise


@router.get("/{id}", response_model=Fixture, status_code=status.HTTP_200_OK)
async def get_fixture(
    id: int,
    fixture_service: Annotated[FixtureService, Depends(get_fixture_service)],
) -> Fixture:
    return await fixture_service.get_fixture_by_id(id)


@router.post("", response_model=Id, status_code=status.HTTP_201_CREATED)
async def create_fixture(
    fixture: FixtureCreate,
    fixture_service: Annotated[FixtureService, Depends(get_fixture_service)],
) -> Id:
    return await fixture_service.create_fixture(fixture)


@router.patch(
    "/{id}", response_model=AcknowledgeMessage, status_code=status.HTTP_200_OK
)
async def update_fixture(
    id: int,
    fixture: FixtureUpdate,
    fixture_service: Annotated[FixtureService, Depends(get_fixture_service)],
) -> AcknowledgeMessage:
    return await fixture_service.update_fixture(id, fixture)


@router.delete(
    "/{id}", response_model=AcknowledgeMessage, status_code=status.HTTP_200_OK
)
async def delete_fixture(
    id: int,
    fixture_service: Annotated[FixtureService, Depends(get_fixture_service)],
) -> AcknowledgeMessage:
    return await fixture_service.delete_fixture(id)
