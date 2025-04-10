from datetime import datetime

from sqlalchemy import select, func, Select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.dao import IRepository
from src.api.fixture.schema import Fixture
from src.db.models.fixture_model import FixtureModel
from src.schemas import Pagination, DAOGetAllParams, IdName

ParentFixture = aliased(FixtureModel)


class FixtureDAO(IRepository[FixtureModel, Fixture]):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_fixture(self, fixture: Fixture, external_id: str) -> int | None:
        fixture_content = fixture.model_dump(exclude_none=True)
        new_fixture = FixtureModel(**fixture_content)
        new_fixture.externalId = external_id
        try:
            self.session.add(new_fixture)
            await self.session.commit()
            await self.session.refresh(new_fixture)
            return new_fixture.id
        except Exception as e:
            print(f"Handle error {e}")
            return None

    async def update_fixture(self, id: int, fixture: Fixture) -> FixtureModel | None:
        try:
            fixture_result = await self.session.execute(
                select(FixtureModel).where(FixtureModel.id == id)
            )
            fixture_result = fixture_result.scalar_one_or_none()
            if fixture_result:
                fixture_content = fixture.model_dump(exclude_none=True)

                update_model = FixtureModel(**fixture_content)
                for key, value in fixture.model_dump(exclude_none=True).items():
                    if key != "id" and hasattr(update_model, key):
                        model_value = getattr(update_model, key)
                        setattr(fixture_result, key, model_value)
                setattr(fixture_result, "updatedAt", datetime.now())
                try:
                    await self.session.commit()
                    return fixture_result
                except Exception:
                    await self.session.rollback()
                    print(f"Error updating Fixture record id: {id}")
            else:
                print("Fixture record not found.")
        except Exception as e:
            print(f"Handle error {e}")

    async def upsert(self, external_id: str, fixture: Fixture) -> None:
        try:
            result = await self.session.execute(
                select(FixtureModel).where(FixtureModel.externalId == external_id)
            )
            result_fixture = result.scalar_one_or_none()

            if result_fixture:
                await self.update_fixture(result_fixture.id, fixture)
            else:
                await self.create_fixture(fixture, external_id)
        except Exception as e:
            print(f"Handle error {e}, id: {external_id}")
            return None

    async def get_fixtures(self, params: DAOGetAllParams) -> Pagination[Fixture]:
        query = select(FixtureModel)
        query = self._get_search_query(query, params)

        total_count = await self.session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        query = query.limit(params.limit).offset(params.offset)

        results = await self.session.execute(query)
        fixtures = list(results.scalars().fetchall())

        count = len(fixtures)
        remaining = max(0, total_count - (count + params.offset))

        result = []

        for fixture in fixtures:
            fixture_instance = Fixture.model_validate(fixture)
            result.append(Fixture(**fixture_instance.model_dump()))

        return Pagination[Fixture](
            cursor=params.offset,
            count=count,
            remaining=remaining,
            results=result,
        )

    async def _get_fixture_by(self, query: Select):
        try:
            result = await self.session.execute(query)
            result = result.scalar_one_or_none()
            return result
        except Exception as e:
            print(f"Handle error {e}")
            return None

    async def get_fixture_by_id(self, id: int) -> Fixture | None:
        query = select(FixtureModel).where(FixtureModel.id == id)
        return await self._get_fixture_by(query)

    async def get_fixture_by_name(self, name: str) -> Fixture | None:
        query = select(FixtureModel).where(FixtureModel.name == name)
        return await self._get_fixture_by(query)

    async def get_fixture_by_external_id(self, external_id: str) -> Fixture | None:
        query = select(FixtureModel).where(FixtureModel.externalId == external_id)
        return await self._get_fixture_by(query)

    async def delete_fixture(self, id: int) -> None:
        try:
            query = select(FixtureModel).where(FixtureModel.id == id)
            result = await self.session.execute(query)
            result = result.scalar_one_or_none()
            external_id = result.externalId

            if result:
                try:
                    await self.session.delete(result)
                    await self.session.commit()
                    return external_id
                except Exception as e:
                    await self.session.rollback()
                    print(f"Error delete Fixture record: {e}")
            else:
                print("Fixture record not found.")
        except Exception as e:
            print(f"Handle error {e}")
            return None
