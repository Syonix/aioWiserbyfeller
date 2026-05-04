"""Tests for the buttons API endpoints."""

import pytest

from aiowiserbyfeller import Button
from aiowiserbyfeller.enum import BlinkPattern

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251

BUTTON_DATA = {
    "id": 101,
    "device": "0000a98f",
    "channel": 0,
    "type": "button",
    "sub_type": "up down",
}


@pytest.mark.asyncio
async def test_async_get_buttons(client_api_auth, mock_aioresponse):
    """Test async_get_buttons."""
    response_json = {
        "status": "success",
        "data": [
            BUTTON_DATA,
            {
                "id": None,
                "device": "0000a98f",
                "channel": 1,
                "type": "button",
                "sub_type": "up down",
            },
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/buttons", "get", response_json
    )

    actual = await client_api_auth.async_get_buttons()

    assert len(actual) == 2
    assert isinstance(actual[0], Button)
    assert actual[0].id == 101
    assert actual[0].device == "0000a98f"
    assert actual[0].channel == 0
    assert actual[0].type == "button"
    assert actual[0].sub_type == "up down"
    assert actual[1].id is None


@pytest.mark.asyncio
async def test_async_create_button(client_api_auth, mock_aioresponse):
    """Test async_create_button."""
    response_json = {"status": "success", "data": [BUTTON_DATA]}
    request_json = {"device": "0000a98f", "channel": 0, "job": 8}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/buttons", "post", response_json, request_json
    )

    actual = await client_api_auth.async_create_button("0000a98f", 0, job=8)

    assert len(actual) == 1
    assert isinstance(actual[0], Button)
    assert actual[0].id == 101

    # Without optional job
    response_no_job = {
        "status": "success",
        "data": [
            {
                "id": 102,
                "device": "0000a98f",
                "channel": 1,
                "type": "button",
                "sub_type": "",
            }
        ],
    }
    request_no_job = {"device": "0000a98f", "channel": 1}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/buttons", "post", response_no_job, request_no_job
    )

    actual = await client_api_auth.async_create_button("0000a98f", 1)

    assert len(actual) == 1
    assert actual[0].id == 102


@pytest.mark.asyncio
async def test_async_get_button(client_api_auth, mock_aioresponse):
    """Test async_get_button."""
    response_json = {"status": "success", "data": BUTTON_DATA}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/buttons/101", "get", response_json
    )

    actual = await client_api_auth.async_get_button(101)

    assert isinstance(actual, Button)
    assert actual.id == 101
    assert actual.device == "0000a98f"


@pytest.mark.asyncio
async def test_async_patch_button(client_api_auth, mock_aioresponse):
    """Test async_patch_button."""
    response_json = {"status": "success", "data": {**BUTTON_DATA, "name": "My Button"}}
    request_json = {"name": "My Button"}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/buttons/101",
        "patch",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_patch_button(101, {"name": "My Button"})

    assert isinstance(actual, Button)
    assert actual.id == 101
    assert actual.raw_data.get("name") == "My Button"


@pytest.mark.asyncio
async def test_async_delete_button(client_api_auth, mock_aioresponse):
    """Test async_delete_button."""
    response_json = {"status": "success", "data": BUTTON_DATA}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/buttons/101", "delete", response_json
    )

    actual = await client_api_auth.async_delete_button(101)

    assert isinstance(actual, Button)
    assert actual.id == 101


@pytest.mark.asyncio
async def test_async_get_managed_buttons(client_api_auth, mock_aioresponse):
    """Test async_get_managed_buttons."""
    response_json = {"status": "success", "data": [BUTTON_DATA]}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/buttons/managed", "get", response_json
    )

    actual = await client_api_auth.async_get_managed_buttons()

    assert len(actual) == 1
    assert isinstance(actual[0], Button)
    assert actual[0].id == 101


@pytest.mark.asyncio
async def test_async_find_buttons(client_api_auth, mock_aioresponse):
    """Test async_find_buttons."""
    response_json = {
        "status": "success",
        "data": {"on": True, "time": 2, "blink_pattern": "ramp", "color": "#806000"},
    }
    request_json = {"on": True, "time": 2, "blink_pattern": "ramp", "color": "#806000"}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/buttons/findme",
        "put",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_find_buttons(
        True, 2, BlinkPattern.RAMP, "#806000"
    )

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_ping_button(client_api_auth, mock_aioresponse):
    """Test async_ping_button."""
    response_json = {
        "status": "success",
        "data": {"time_ms": 3000, "blink_pattern": "slow", "color": "#ff0000"},
    }
    request_json = {"time_ms": 3000, "blink_pattern": "slow", "color": "#ff0000"}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/buttons/101/ping",
        "put",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_ping_button(
        101, 3000, BlinkPattern.SLOW, "#ff0000"
    )

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_button_async_refresh(client_api_auth, mock_aioresponse):
    """Test Button.async_refresh."""
    updated_data = {**BUTTON_DATA, "sub_type": "toggle"}
    response_json = {"status": "success", "data": updated_data}

    button = Button(BUTTON_DATA, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/buttons/101", "get", response_json
    )

    await button.async_refresh()

    assert button.id == 101
    assert button.sub_type == "toggle"


@pytest.mark.asyncio
async def test_button_async_ping(client_api_auth, mock_aioresponse):
    """Test Button.async_ping."""
    response_json = {
        "status": "success",
        "data": {"time_ms": 2000, "blink_pattern": "ramp", "color": "#505050"},
    }
    request_json = {"time_ms": 2000, "blink_pattern": "ramp", "color": "#505050"}

    button = Button(BUTTON_DATA, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/buttons/101/ping",
        "put",
        response_json,
        request_json,
    )

    await button.async_ping(2000, BlinkPattern.RAMP, "#505050")
