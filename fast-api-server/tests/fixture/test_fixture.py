import uuid

import pytest
from fastapi import FastAPI, HTTPException
from httpx import AsyncClient
from starlette import status
from unittest.mock import MagicMock, AsyncMock, patch

from tests.fixture.mocks import (
    EXTERNAL_LO_FIXTURES_MOCK,
    EXTERNAL_LO_FIXTURE_MOCK,
    EXTERNAL_FIXTURE_MOCK,
    EXTERNAL_ID_RESPONSE_MOCK,
)


@pytest.mark.anyio
async def test_get_fixtures_list_success(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_requests_request,
    patch_verify,
    mock_fixture_dao,
) -> None:
    mock_response = MagicMock()

    mock_response.json.return_value = EXTERNAL_LO_FIXTURES_MOCK
    mock_response.status_code = 200
    mock_requests_request.return_value = mock_response

    url = fastapi_app.url_path_for("get_fixtures")

    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK, "Status code is 200"


@pytest.mark.anyio
async def test_get_by_correct_id(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_requests_request,
    patch_verify,
    mock_fixture_dao,
) -> None:
    mock_id = "334896062483722700"
    mock_response = MagicMock()

    mock_response.json.return_value = EXTERNAL_LO_FIXTURE_MOCK
    mock_response.status_code = 200
    mock_requests_request.return_value = mock_response
    url = fastapi_app.url_path_for("get_fixture", id=mock_id)
    response = await client.get(url)
    response_body = response.json()
    assert response.status_code == status.HTTP_200_OK, "Status code is 200"
    assert response_body["id"] == mock_id, "Correct id"


@pytest.mark.anyio
async def test_get_by_incorrect_id(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_requests_request,
    patch_verify,
    mock_fixture_dao,
) -> None:
    mock_id = uuid.uuid4()
    mock_response = MagicMock()

    url = fastapi_app.url_path_for("get_fixture", id=mock_id)

    mock_response.json.return_value = {}
    mock_response.status_code = 422
    mock_response.raise_for_status.return_value = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPException(
        422, "Fixture is not found", None
    )
    mock_requests_request.return_value = mock_response
    response = await client.get(url)
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), "Status code is 422"


@pytest.mark.anyio
async def test_post_success(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_requests_request,
    patch_verify,
    mock_fixture_dao,
) -> None:
    mock_id = "334896062483722700"
    mock_response = MagicMock()

    mock_response.json.return_value = EXTERNAL_ID_RESPONSE_MOCK
    mock_response.status_code = 200
    mock_requests_request.return_value = mock_response
    url = fastapi_app.url_path_for("create_fixture")
    response = await client.post(url, json=EXTERNAL_FIXTURE_MOCK)
    response_body = response.json()
    assert response.status_code == status.HTTP_201_CREATED, "Status code is 201"
    assert response_body["id"] == mock_id, "Correct id"


@pytest.mark.anyio
async def test_post_fails(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_requests_request,
    patch_verify,
    mock_fixture_dao,
) -> None:
    mock_response = MagicMock()

    url = fastapi_app.url_path_for("create_fixture")

    mock_response.json.return_value = {}
    mock_response.status_code = 422
    mock_response.raise_for_status.return_value = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPException(
        422, "Failed to create", None
    )
    mock_requests_request.return_value = mock_response
    response = await client.post(url, json=EXTERNAL_FIXTURE_MOCK)
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), "Status code is 422"


@pytest.mark.anyio
async def test_patch_success(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_requests_request,
    patch_verify,
    mock_fixture_dao,
) -> None:
    mock_id = "334896062483722700"
    mock_response = MagicMock()

    mock_response.json.return_value = EXTERNAL_ID_RESPONSE_MOCK
    mock_response.status_code = 200
    mock_requests_request.return_value = mock_response
    url = fastapi_app.url_path_for("update_fixture", id=mock_id)
    response = await client.patch(url, json=EXTERNAL_FIXTURE_MOCK)
    response_body = response.json()
    assert response.status_code == status.HTTP_200_OK, "Status code is 200"
    assert response_body["message"] == "Success", "Correct message"


@pytest.mark.anyio
async def test_patch_fails(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_requests_request,
    patch_verify,
    mock_fixture_dao,
) -> None:
    mock_id = "334896062483722700"
    mock_response = MagicMock()

    url = fastapi_app.url_path_for("update_fixture", id=mock_id)

    mock_response.json.return_value = {}
    mock_response.status_code = 422
    mock_response.raise_for_status.return_value = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPException(
        422, "Failed to update", None
    )
    mock_requests_request.return_value = mock_response
    response = await client.patch(url, json=EXTERNAL_FIXTURE_MOCK)
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), "Status code is 422"


@pytest.mark.anyio
async def test_delete_success(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_requests_request,
    patch_verify,
    mock_fixture_dao,
) -> None:
    mock_id = "334896062483722700"
    mock_response = MagicMock()

    mock_response.json.return_value = EXTERNAL_ID_RESPONSE_MOCK
    mock_response.status_code = 200
    mock_requests_request.return_value = mock_response
    url = fastapi_app.url_path_for("delete_fixture", id=mock_id)
    response = await client.delete(url)
    response_body = response.json()
    assert response.status_code == status.HTTP_200_OK, "Status code is 200"
    assert response_body["message"] == "Success", "Correct message"


@pytest.mark.anyio
async def test_delete_fails(
    client: AsyncClient,
    fastapi_app: FastAPI,
    mock_requests_request,
    patch_verify,
    mock_fixture_dao,
) -> None:
    mock_id = "334896062483722700"
    mock_response = MagicMock()

    url = fastapi_app.url_path_for("delete_fixture", id=mock_id)

    mock_response.json.return_value = {}
    mock_response.status_code = 422
    mock_response.raise_for_status.return_value = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPException(
        422, "Failed to delete", None
    )
    mock_requests_request.return_value = mock_response
    response = await client.delete(url)
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    ), "Status code is 422"

@pytest.fixture
def mock_requests_request():
    with patch("requests.request") as mock_request:
        yield mock_request

@pytest.fixture
def mock_fixture_dao():
    with patch("src.api.fixture.service.FixtureDAO") as MockFixtureDAO:
        # Setup the mock instance methods.
        mock_instance = MockFixtureDAO.return_value
        mock_instance.get_fixture_by_id = AsyncMock(return_value=None)
        mock_instance.create_fixture = AsyncMock(return_value=MagicMock(id="test"))
        mock_instance.update_fixture = AsyncMock(return_value=MagicMock(None))
        mock_instance.upsert = AsyncMock(return_value=MagicMock(None))
        mock_instance.delete_fixture = AsyncMock(return_value=MagicMock(None))

        yield MockFixtureDAO