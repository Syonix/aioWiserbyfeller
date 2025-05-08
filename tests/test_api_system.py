"""aiowiserbyfeller Api system tests."""

import pytest

from aiowiserbyfeller import SystemCondition, SystemFlag

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_system_flags(client_api_auth, mock_aioresponse):
    """Test async_get_system_flags."""
    response_json = {
        "status": "success",
        "data": [{"id": 2, "symbol": "cleaning", "value": True, "name": "Putzen"}],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/system/flags", "get", response_json
    )

    actual = await client_api_auth.async_get_system_flags()

    assert len(actual) == 1
    assert isinstance(actual[0], SystemFlag)
    assert actual[0].id == 2
    assert actual[0].name == "Putzen"


@pytest.mark.asyncio
async def test_async_create_system_flag(client_api_auth, mock_aioresponse):
    """Test async_create_system_flag."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "symbol": "cleaning", "value": True, "name": "Putzen"},
    }

    request_json = {"symbol": "cleaning", "value": True, "name": "Putzen"}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/system/flags",
        "post",
        response_json,
        request_json,
    )

    flag = SystemFlag(request_json, client_api_auth)
    actual = await client_api_auth.async_create_system_flag(flag)

    assert isinstance(actual, SystemFlag)
    assert actual.id == 2
    assert actual.name == "Putzen"


@pytest.mark.asyncio
async def test_async_get_system_flag(client_api_auth, mock_aioresponse):
    """Test async_get_system_flag."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "symbol": "cleaning", "value": True, "name": "Putzen"},
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/system/flags/2", "get", response_json
    )

    actual = await client_api_auth.async_get_system_flag(2)

    assert isinstance(actual, SystemFlag)
    assert actual.id == 2
    assert actual.name == "Putzen"


@pytest.mark.asyncio
async def test_system_flag_async_update(client_api_auth, mock_aioresponse):
    """Test system_flag_async_update."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "symbol": "cleaning", "value": True, "name": "Putzen"},
    }

    request_json = {"id": 2, "symbol": "cleaning", "value": True, "name": "Putzen"}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/system/flags/2",
        "patch",
        response_json,
        request_json,
    )

    flag = SystemFlag(
        {"id": 2, "symbol": "cleaning", "value": True, "name": "Putzen"},
        client_api_auth.auth,
    )

    actual = await client_api_auth.async_update_system_flag(flag)
    assert actual.symbol == "cleaning"


@pytest.mark.asyncio
async def test_async_delete_system_flag(client_api_auth, mock_aioresponse):
    """Test async_delete_system_flag."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "symbol": "cleaning", "value": True, "name": "Putzen"},
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/system/flags/2", "delete", response_json
    )

    actual = await client_api_auth.async_delete_system_flag(2)

    assert isinstance(actual, SystemFlag)
    assert actual.id == 2
    assert actual.name == "Putzen"


@pytest.mark.asyncio
async def test_system_flag_async_refresh(client_api_auth, mock_aioresponse):
    """Test SystemFlag.async_refresh."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "symbol": "cleaning", "value": True, "name": "Putzen Neu"},
    }

    raw_data = {"id": 2, "symbol": "cleaning", "value": False, "name": "Putzen"}

    flag = SystemFlag(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/system/flags/2", "get", response_json
    )

    await flag.async_refresh()

    assert flag.id == 2
    assert flag.symbol == "cleaning"
    assert flag.name == "Putzen Neu"
    assert flag.value is True


@pytest.mark.asyncio
async def test_async_get_system_conditions(client_api_auth, mock_aioresponse):
    """Test async_get_system_conditions."""
    response_json = {
        "status": "success",
        "data": [
            {"id": 6, "value": True, "expression": "not absent", "name": "Anwesend"}
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/system/conditions", "get", response_json
    )

    actual = await client_api_auth.async_get_system_conditions()

    assert len(actual) == 1
    assert isinstance(actual[0], SystemCondition)
    assert actual[0].id == 6
    assert actual[0].expression == "not absent"


@pytest.mark.asyncio
async def test_async_create_system_condition(client_api_auth, mock_aioresponse):
    """Test async_create_system_condition."""
    response_json = {
        "status": "success",
        "data": {
            "id": 6,
            "value": True,
            "expression": "not absent",
            "name": "Anwesend",
        },
    }

    request_json = {"expression": "not absent", "name": "Anwesend"}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/system/conditions",
        "post",
        response_json,
        request_json,
    )

    condition = SystemCondition(request_json, client_api_auth)

    actual = await client_api_auth.async_create_system_condition(condition)

    assert isinstance(actual, SystemCondition)
    assert actual.id == 6
    assert actual.expression == "not absent"


@pytest.mark.asyncio
async def test_async_get_system_condition(client_api_auth, mock_aioresponse):
    """Test async_get_system_condition."""
    response_json = {
        "status": "success",
        "data": {
            "id": 6,
            "value": True,
            "expression": "not absent",
            "name": "Anwesend",
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/system/conditions/6", "get", response_json
    )

    actual = await client_api_auth.async_get_system_condition(6)

    assert isinstance(actual, SystemCondition)
    assert actual.id == 6
    assert actual.expression == "not absent"


@pytest.mark.asyncio
async def test_async_patch_system_condition(client_api_auth, mock_aioresponse):
    """Test async_patch_system_condition."""
    response_json = {
        "status": "success",
        "data": {
            "id": 6,
            "value": True,
            "expression": "not absent",
            "name": "Anwesend",
        },
    }

    request_json = {
        "expression": "not absent",
        "name": "Anwesend",
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/system/conditions/6",
        "patch",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_patch_system_condition(6, request_json)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_update_system_condition(client_api_auth, mock_aioresponse):
    """Test async_update_system_condition."""
    response_json = {
        "status": "success",
        "data": {
            "id": 6,
            "value": True,
            "expression": "not absent",
            "name": "Anwesend",
        },
    }

    request_json = {
        "id": 6,
        "value": True,
        "expression": "not absent",
        "name": "Anwesend",
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/system/conditions/6",
        "patch",
        response_json,
        request_json,
    )

    condition = SystemCondition(
        request_json,
        client_api_auth.auth,
    )

    actual = await client_api_auth.async_update_system_condition(condition)
    assert actual.expression == "not absent"


@pytest.mark.asyncio
async def test_async_delete_system_condition(client_api_auth, mock_aioresponse):
    """Test async_delete_system_condition."""
    response_json = {
        "status": "success",
        "data": {
            "id": 6,
            "value": True,
            "expression": "not absent",
            "name": "Anwesend",
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/system/conditions/6", "delete", response_json
    )

    actual = await client_api_auth.async_delete_system_condition(6)

    assert isinstance(actual, SystemCondition)
    assert actual.id == 6
    assert actual.expression == "not absent"


@pytest.mark.asyncio
async def test_system_condition_async_refresh(client_api_auth, mock_aioresponse):
    """Test SystemCondition.async_refresh."""
    response_json = {
        "status": "success",
        "data": {
            "id": 6,
            "value": True,
            "expression": "not absent",
            "name": "Anwesend Neu",
        },
    }

    raw_data = {
        "id": 6,
        "value": False,
        "expression": "not absent",
        "name": "Anwesend",
    }

    condition = SystemCondition(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/system/conditions/6", "get", response_json
    )

    await condition.async_refresh()

    assert condition.id == 6
    assert condition.value is True
    assert condition.expression == "not absent"
    assert condition.name == "Anwesend Neu"
