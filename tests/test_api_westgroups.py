"""aiowiserbyfeller Api class WEST-Groups tests."""

import pytest

from aiowiserbyfeller import WestGroup

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251

WESTGROUP_RAW = {
    "id": 6,
    "loads": [42, 24, 56],
    "wind": {"action": "up", "threshold": 5.5, "unit": "m/s"},
    "temperature": {"action": "off", "threshold": 1.5, "unit": "°C"},
    "rain": {"action": "off", "unit": "bool"},
    "hail": {"action": "up and lock", "unit": "bool"},
}


@pytest.mark.asyncio
async def test_async_get_westgroups(client_api_auth, mock_aioresponse):
    """Test async_get_westgroups."""
    response_json = {"status": "success", "data": [WESTGROUP_RAW]}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/westgroups", "get", response_json
    )

    actual = await client_api_auth.async_get_westgroups()

    assert len(actual) == 1
    assert isinstance(actual[0], WestGroup)
    assert actual[0].id == 6
    assert actual[0].loads == [42, 24, 56]
    assert actual[0].wind["action"] == "up"
    assert actual[0].hail["action"] == "up and lock"


@pytest.mark.asyncio
async def test_async_create_westgroup(client_api_auth, mock_aioresponse):
    """Test async_create_westgroup."""
    request_json = {"loads": [42, 24, 56]}
    response_json = {"status": "success", "data": {**WESTGROUP_RAW}}

    westgroup = WestGroup(request_json, client_api_auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/westgroups",
        "post",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_create_westgroup(westgroup)

    assert isinstance(actual, WestGroup)
    assert actual.id == 6
    assert actual.loads == [42, 24, 56]


@pytest.mark.asyncio
async def test_async_get_westgroup(client_api_auth, mock_aioresponse):
    """Test async_get_westgroup."""
    response_json = {"status": "success", "data": WESTGROUP_RAW}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/westgroups/6", "get", response_json
    )

    actual = await client_api_auth.async_get_westgroup(6)

    assert isinstance(actual, WestGroup)
    assert actual.id == 6
    assert actual.wind["threshold"] == 5.5


@pytest.mark.asyncio
async def test_async_update_westgroup(client_api_auth, mock_aioresponse):
    """Test async_update_westgroup."""
    request_json = {**WESTGROUP_RAW, "loads": [80, 81]}
    response_json = {"status": "success", "data": {**WESTGROUP_RAW, "loads": [80, 81]}}

    westgroup = WestGroup(request_json, client_api_auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/westgroups/6",
        "put",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_update_westgroup(westgroup)

    assert isinstance(actual, WestGroup)
    assert actual.loads == [80, 81]


@pytest.mark.asyncio
async def test_async_patch_westgroup(client_api_auth, mock_aioresponse):
    """Test async_patch_westgroup."""
    request_json = {"loads": [80, 81]}
    response_json = {
        "status": "success",
        "data": {**WESTGROUP_RAW, "loads": [42, 24, 56, 80, 81]},
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/westgroups/6",
        "patch",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_patch_westgroup(6, request_json)

    assert isinstance(actual, WestGroup)
    assert 80 in actual.loads
    assert 81 in actual.loads


@pytest.mark.asyncio
async def test_async_delete_westgroup(client_api_auth, mock_aioresponse):
    """Test async_delete_westgroup."""
    response_json = {"status": "success", "data": WESTGROUP_RAW}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/westgroups/6", "delete", response_json
    )

    actual = await client_api_auth.async_delete_westgroup(6)

    assert isinstance(actual, WestGroup)
    assert actual.id == 6


@pytest.mark.asyncio
async def test_async_bind_westgroup(client_api_auth, mock_aioresponse):
    """Test async_bind_westgroup."""
    response_json = {
        "status": "success",
        "data": {
            **WESTGROUP_RAW,
            "weather_station_ref": {"address": "0x00000124"},
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/westgroups/6/bind", "patch", response_json
    )

    actual = await client_api_auth.async_bind_westgroup(6)

    assert isinstance(actual, WestGroup)
    assert actual.id == 6
    assert actual.raw_data["weather_station_ref"]["address"] == "0x00000124"


@pytest.mark.asyncio
async def test_async_delete_westgroup_bind(client_api_auth, mock_aioresponse):
    """Test async_delete_westgroup_bind."""
    response_json = {"status": "success", "data": WESTGROUP_RAW}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/westgroups/6/bind", "delete", response_json
    )

    actual = await client_api_auth.async_delete_westgroup_bind(6)

    assert isinstance(actual, WestGroup)
    assert actual.id == 6


@pytest.mark.asyncio
async def test_async_get_westgroup_test(client_api_auth, mock_aioresponse):
    """Test async_get_westgroup_test."""
    test_data = {"keep_alive": 600, "wind": 20.0, "rain": False, "hail": False}
    response_json = {"status": "success", "data": test_data}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/westgroups/test", "get", response_json
    )

    actual = await client_api_auth.async_get_westgroup_test()
    assert actual == test_data


@pytest.mark.asyncio
async def test_async_start_westgroup_test(client_api_auth, mock_aioresponse):
    """Test async_start_westgroup_test."""
    request_json = {"wind": 20.0, "rain": False, "hail": False}
    test_data = {"keep_alive": 600, **request_json}
    response_json = {"status": "success", "data": test_data}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/westgroups/test",
        "put",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_start_westgroup_test(request_json)
    assert actual == test_data


@pytest.mark.asyncio
async def test_async_extend_westgroup_test(client_api_auth, mock_aioresponse):
    """Test async_extend_westgroup_test."""
    test_data = {"keep_alive": 1200, "wind": 20.0}
    response_json = {"status": "success", "data": test_data}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/westgroups/test", "patch", response_json
    )

    actual = await client_api_auth.async_extend_westgroup_test()
    assert actual == test_data


@pytest.mark.asyncio
async def test_async_stop_westgroup_test(client_api_auth, mock_aioresponse):
    """Test async_stop_westgroup_test."""
    test_data = {"keep_alive": 0}
    response_json = {"status": "success", "data": test_data}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/westgroups/test", "delete", response_json
    )

    actual = await client_api_auth.async_stop_westgroup_test()
    assert actual == test_data


@pytest.mark.asyncio
async def test_westgroup_async_refresh(client_api_auth, mock_aioresponse):
    """Test WestGroup.async_refresh."""
    response_json = {"status": "success", "data": WESTGROUP_RAW}

    westgroup = WestGroup({"id": 6, "loads": []}, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/westgroups/6", "get", response_json
    )

    await westgroup.async_refresh()

    assert westgroup.id == 6
    assert westgroup.loads == [42, 24, 56]
    assert westgroup.wind["action"] == "up"
