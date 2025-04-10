from typing import cast

from src.api.commons.contracts import PaginationContract
from src.api.commons.mappers import convert_to_entities
from src.schemas import Pagination
from src.api.fixture.schema import ExternalFixture, Fixture


def external_fixture_to_fixture(model: ExternalFixture) -> Fixture:
    model = cast(dict, model)

    return Fixture(
        externalId=model.get("_id"),
        modifiedDate=model.get("Modified Date"),
        createdDate=model.get("Created Date"),
        createdBy=model.get("Created By"),
        name=model.get("Name"),
        fixtureUrl=model.get("Fixture url"),
        demo=model.get("Demo"),
        statuses=model.get("Statuses"),
    )


def fixture_to_external_fixture(model: Fixture) -> ExternalFixture:
    return ExternalFixture(
        name=model.name,
        fixture_url=model.scheduleUrl,
        demo=model.demo,
        statuses=model.statuses,
    )


def pagination_external_fixture_to_pagination_ge(
    model: PaginationContract[ExternalFixture],
) -> Pagination[Fixture]:
    return convert_to_entities(model, external_fixture_to_fixture)
