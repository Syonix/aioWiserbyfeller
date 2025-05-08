"""aiowiserbyfeller Api class rooms tests."""

import pytest

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_rooms(client_api_auth, mock_aioresponse):
    """Test async_get_rooms."""
    response_json = {
        "status": "success",
        "data": [{"id": 0, "name": "Tom's room", "kind": 12, "load_order": [7, 15, 8]}],
    }
    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/rooms", "get", response_json
    )

    actual = await client_api_auth.async_get_rooms()
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_create_room(client_api_auth, mock_aioresponse):
    """Test async_create_room."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "name": "Tina's room", "kind": 12},
    }

    request_json = {"name": "Tina's room", "kind": 12}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/rooms", "post", response_json, request_json
    )

    actual = await client_api_auth.async_create_room(request_json)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_room(client_api_auth, mock_aioresponse):
    """Test async_get_room."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "name": "Tina's room", "kind": 12},
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/rooms/2", "get", response_json
    )

    actual = await client_api_auth.async_get_room(2)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_update_room(client_api_auth, mock_aioresponse):
    """Test async_update_room."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "name": "Tina's play room", "kind": 12},
    }

    request_json = {"name": "Tina's play room"}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/rooms/2", "patch", response_json, request_json
    )

    actual = await client_api_auth.async_update_room(2, request_json)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_delete_room(client_api_auth, mock_aioresponse):
    """Test async_delete_room."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "name": "Tina's room", "kind": 12},
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/rooms/2", "delete", response_json
    )

    actual = await client_api_auth.async_delete_room(2)
    assert actual == response_json["data"]
