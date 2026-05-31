"""aiowiserbyfeller Api class Group Ctrls tests."""

import pytest

from aiowiserbyfeller import GroupCtrl

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251

GROUPCTRL_RAW = {
    "id": 3,
    "name": "Candlelight Dinner",
    "type": "light",
}


@pytest.mark.asyncio
async def test_async_get_group_ctrls(client_api_auth, mock_aioresponse):
    """Test async_get_group_ctrls."""
    response_json = {"status": "success", "data": [GROUPCTRL_RAW]}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/groupctrls", "get", response_json
    )

    actual = await client_api_auth.async_get_group_ctrls()

    assert len(actual) == 1
    assert isinstance(actual[0], GroupCtrl)
    assert actual[0].id == 3
    assert actual[0].name == "Candlelight Dinner"
    assert actual[0].type == "light"


@pytest.mark.asyncio
async def test_async_create_group_ctrl(client_api_auth, mock_aioresponse):
    """Test async_create_group_ctrl."""
    request_json = {"name": "Candlelight Dinner", "type": "light"}
    response_json = {"status": "success", "data": {**request_json, "id": 3}}

    group_ctrl = GroupCtrl(request_json, client_api_auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/groupctrls",
        "post",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_create_group_ctrl(group_ctrl)

    assert isinstance(actual, GroupCtrl)
    assert actual.id == 3
    assert actual.name == "Candlelight Dinner"
    assert actual.type == "light"


@pytest.mark.asyncio
async def test_async_get_group_ctrl(client_api_auth, mock_aioresponse):
    """Test async_get_group_ctrl."""
    response_json = {"status": "success", "data": GROUPCTRL_RAW}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/groupctrls/3", "get", response_json
    )

    actual = await client_api_auth.async_get_group_ctrl(3)

    assert isinstance(actual, GroupCtrl)
    assert actual.id == 3
    assert actual.name == "Candlelight Dinner"


@pytest.mark.asyncio
async def test_async_update_group_ctrl(client_api_auth, mock_aioresponse):
    """Test async_update_group_ctrl."""
    request_json = {**GROUPCTRL_RAW, "name": "Dinner Party"}
    response_json = {"status": "success", "data": request_json}

    group_ctrl = GroupCtrl(request_json, client_api_auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/groupctrls/3",
        "put",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_update_group_ctrl(group_ctrl)

    assert isinstance(actual, GroupCtrl)
    assert actual.id == 3
    assert actual.name == "Dinner Party"


@pytest.mark.asyncio
async def test_async_patch_group_ctrl(client_api_auth, mock_aioresponse):
    """Test async_patch_group_ctrl."""
    request_json = {"name": "Dinner Party"}
    response_json = {
        "status": "success",
        "data": {**GROUPCTRL_RAW, "name": "Dinner Party"},
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/groupctrls/3",
        "patch",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_patch_group_ctrl(3, request_json)

    assert isinstance(actual, GroupCtrl)
    assert actual.id == 3
    assert actual.name == "Dinner Party"


@pytest.mark.asyncio
async def test_async_delete_group_ctrl(client_api_auth, mock_aioresponse):
    """Test async_delete_group_ctrl."""
    response_json = {"status": "success", "data": GROUPCTRL_RAW}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/groupctrls/3", "delete", response_json
    )

    actual = await client_api_auth.async_delete_group_ctrl(3)

    assert isinstance(actual, GroupCtrl)
    assert actual.id == 3
    assert actual.name == "Candlelight Dinner"


@pytest.mark.asyncio
async def test_group_ctrl_async_refresh(client_api_auth, mock_aioresponse):
    """Test GroupCtrl.async_refresh."""
    response_json = {"status": "success", "data": GROUPCTRL_RAW}

    group_ctrl = GroupCtrl({"id": 3, "name": "Old name"}, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/groupctrls/3", "get", response_json
    )

    await group_ctrl.async_refresh()

    assert group_ctrl.id == 3
    assert group_ctrl.name == "Candlelight Dinner"
    assert group_ctrl.type == "light"
