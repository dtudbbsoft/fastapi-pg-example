from typing import cast

from src.api.commons.contracts import PaginationContract
from src.api.commons.mappers import convert_to_entities
from src.schemas import Pagination
from src.api.fixture.schema import ExternalFixture, Fixture


def bubble_geo_to_geo(model: ExternalFixture) -> Fixture:
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


def geo_to_bubble_geo(model: Fixture) -> ExternalFixture:
    return ExternalFixture(
        name=model.name,
        fixture_url=model.scheduleUrl,
        demo=model.demo,
        statuses=model.statuses,
    )


def pagination_bubble_geo_to_pagination_ge(
    model: PaginationContract[ExternalFixture],
) -> Pagination[Fixture]:
    return convert_to_entities(model, bubble_geo_to_geo)
