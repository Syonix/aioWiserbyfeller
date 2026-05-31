"""aiowiserbyfeller Api class schedulers tests."""

import pytest

from aiowiserbyfeller import Scheduler

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251

SCHEDULER_RAW = {
    "id": 7,
    "name": "Morning hallway light scheduling",
    "icon": "tree.png",
}


@pytest.mark.asyncio
async def test_async_get_schedulers(client_api_auth, mock_aioresponse):
    """Test async_get_schedulers."""
    response_json = {"status": "success", "data": [SCHEDULER_RAW]}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/schedulers", "get", response_json
    )

    actual = await client_api_auth.async_get_schedulers()

    assert len(actual) == 1
    assert isinstance(actual[0], Scheduler)
    assert actual[0].id == 7
    assert actual[0].name == "Morning hallway light scheduling"
    assert actual[0].icon == "tree.png"


@pytest.mark.asyncio
async def test_async_create_scheduler(client_api_auth, mock_aioresponse):
    """Test async_create_scheduler."""
    request_json = {"name": "Morning hallway light scheduling", "kind": 1}
    response_json = {"status": "success", "data": {**request_json, "id": 7}}

    scheduler = Scheduler(request_json, client_api_auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/schedulers",
        "post",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_create_scheduler(scheduler)

    assert isinstance(actual, Scheduler)
    assert actual.id == 7
    assert actual.name == "Morning hallway light scheduling"


@pytest.mark.asyncio
async def test_async_get_scheduler(client_api_auth, mock_aioresponse):
    """Test async_get_scheduler."""
    response_json = {"status": "success", "data": SCHEDULER_RAW}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/schedulers/7", "get", response_json
    )

    actual = await client_api_auth.async_get_scheduler(7)

    assert isinstance(actual, Scheduler)
    assert actual.id == 7
    assert actual.name == "Morning hallway light scheduling"


@pytest.mark.asyncio
async def test_async_update_scheduler(client_api_auth, mock_aioresponse):
    """Test async_update_scheduler."""
    request_json = {"id": 7, "icon": "tree.png"}
    response_json = {"status": "success", "data": {**SCHEDULER_RAW, "icon": "tree.png"}}

    scheduler = Scheduler(request_json, client_api_auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/schedulers/7",
        "put",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_update_scheduler(scheduler)

    assert isinstance(actual, Scheduler)
    assert actual.id == 7
    assert actual.icon == "tree.png"


@pytest.mark.asyncio
async def test_async_patch_scheduler(client_api_auth, mock_aioresponse):
    """Test async_patch_scheduler."""
    request_json = {"name": "Garden scheduling"}
    response_json = {
        "status": "success",
        "data": {**SCHEDULER_RAW, "name": "Garden scheduling"},
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/schedulers/7",
        "patch",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_patch_scheduler(7, request_json)

    assert isinstance(actual, Scheduler)
    assert actual.id == 7
    assert actual.name == "Garden scheduling"


@pytest.mark.asyncio
async def test_async_delete_scheduler(client_api_auth, mock_aioresponse):
    """Test async_delete_scheduler."""
    response_json = {"status": "success", "data": SCHEDULER_RAW}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/schedulers/7", "delete", response_json
    )

    actual = await client_api_auth.async_delete_scheduler(7)

    assert isinstance(actual, Scheduler)
    assert actual.id == 7
    assert actual.name == "Morning hallway light scheduling"


@pytest.mark.asyncio
async def test_scheduler_async_refresh(client_api_auth, mock_aioresponse):
    """Test Scheduler.async_refresh."""
    response_json = {"status": "success", "data": SCHEDULER_RAW}

    scheduler = Scheduler({"id": 7, "name": "Old name"}, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/schedulers/7", "get", response_json
    )

    await scheduler.async_refresh()

    assert scheduler.id == 7
    assert scheduler.name == "Morning hallway light scheduling"
    assert scheduler.icon == "tree.png"
