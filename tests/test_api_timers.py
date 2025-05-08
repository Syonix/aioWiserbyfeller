"""aiowiserbyfeller Api class timers tests."""

import pytest

from aiowiserbyfeller import Timer

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_timers(client_api_auth, mock_aioresponse):
    """Test async_get_timers."""
    response_json = {
        "status": "success",
        "data": [
            {
                "id": 2,
                "enabled": False,
                "job": 3,
                "when": {"every": "Sun,Wed", "at": "23:59"},
            }
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/timers", "get", response_json
    )

    actual = await client_api_auth.async_get_timers()

    assert len(actual) == 1
    assert isinstance(actual[0], Timer)
    assert actual[0].id == 2
    assert actual[0].enabled is False
    assert actual[0].when["every"] == "Sun,Wed"


@pytest.mark.asyncio
async def test_async_create_timer(client_api_auth, mock_aioresponse):
    """Test async_create_timer."""
    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "enabled": False,
            "job": 3,
            "when": {"every": "Sun,Wed", "at": "23:59"},
        },
    }

    request_json = {
        "enabled": False,
        "job": 3,
        "when": {"every": "Sun,Wed", "at": "23:59"},
    }

    timer = Timer(request_json, client_api_auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/timers", "post", response_json, request_json
    )

    actual = await client_api_auth.async_create_timer(timer)

    assert isinstance(actual, Timer)
    assert actual.id == 2
    assert actual.enabled is False
    assert actual.when["every"] == "Sun,Wed"


@pytest.mark.asyncio
async def test_async_update_timer(client_api_auth, mock_aioresponse):
    """Test async_update_timer."""
    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "enabled": False,
            "job": 3,
            "when": {"every": "Sun,Wed", "at": "23:59"},
        },
    }

    request_json = {
        "id": 2,
        "enabled": False,
        "job": 3,
        "when": {"every": "Sun,Wed", "at": "23:59"},
    }

    timer = Timer(request_json, client_api_auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/timers/2", "put", response_json, request_json
    )

    actual = await client_api_auth.async_update_timer(timer)

    assert isinstance(actual, Timer)
    assert actual.id == 2
    assert actual.enabled is False
    assert actual.when["every"] == "Sun,Wed"


@pytest.mark.asyncio
async def test_async_patch_timer(client_api_auth, mock_aioresponse):
    """Test async_patch_timer."""
    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "enabled": False,
            "job": 3,
            "when": {"every": "Sun,Wed", "at": "23:59"},
        },
    }

    request_json = {
        "enabled": False,
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/timers/2", "patch", response_json, request_json
    )

    actual = await client_api_auth.async_patch_timer(2, request_json)

    assert actual["id"] == 2
    assert actual["enabled"] is False
    assert actual["when"]["every"] == "Sun,Wed"


@pytest.mark.asyncio
async def test_async_delete_timer(client_api_auth, mock_aioresponse):
    """Test async_delete_timer."""
    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "enabled": False,
            "job": 3,
            "when": {"every": "Sun,Wed", "at": "23:59"},
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/timers/2", "delete", response_json
    )

    actual = await client_api_auth.async_delete_timer(2)

    assert isinstance(actual, Timer)
    assert actual.id == 2
    assert actual.enabled is False
    assert actual.when["every"] == "Sun,Wed"


@pytest.mark.asyncio
async def test_timer_async_refresh(client_api_auth, mock_aioresponse):
    """Test Timer.async_refresh."""
    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "enabled": False,
            "job": 3,
            "when": {"every": "Sun,Wed", "at": "23:59"},
        },
    }

    raw_data = {
        "id": 2,
        "enabled": True,
        "job": 9,
        "when": {"every": "Sun,Wed", "at": "23:59"},
    }

    timer = Timer(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/timers/2", "get", response_json
    )

    await timer.async_refresh()

    assert timer.id == 2
    assert timer.job == 3
    assert timer.enabled is False
    assert timer.when["every"] == "Sun,Wed"
