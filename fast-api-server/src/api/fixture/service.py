from sqlalchemy.ext.asyncio import AsyncSession
from fast_api_db import get_db_session
from typing import Annotated
from fastapi import Depends

from src.utils.contracts import PaginationContract
from src.utils.dao import IRepository
from src.schemas import Pagination, Id, AcknowledgeMessage, DAOGetAllParams, IdName

from src.api.fixture.schema import (
    Fixture, FixtureCreate, FixtureUpdate, FixtureProperties, ExternalFixture, FixtureSearchQuery
)

EXTERNAL_TABLE_NAME = "fixture"


class FixtureService(ExternalServiceConnector[ExternalFixture, Fixture]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(EXTERNAL_TABLE_NAME)

        self.fixture_dao = FixtureDAO(db_session)
        self.external_service: ExternalService = ExternalService()

    @property
    def repository(self) -> IRepository:
        return self.fixture_dao

    def _external_response_to_entities(self, pagination: PaginationContract[ExternalFixture]) -> Pagination[Fixture]:
        pass

    async def get_fixtures(
        self,
        filters: FixtureSearchQuery
    ) -> Pagination[Fixture]:
        pass

    async def get_fixture_by_id(self, id: int) -> Fixture:
        pass


    async def create_fixture(self, fixture: FixtureCreate) -> Id:
        pass

    async def update_fixture(self, id: int, fixture: FixtureUpdate) -> AcknowledgeMessage:
        pass

    async def delete_fixture(self, id: int) -> AcknowledgeMessage:
        pass


def get_fixture_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> FixtureService:
    return FixtureService(db_session)
