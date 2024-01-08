"""aiowiserbyfeller Api class smart buttons tests"""
import pytest
from .conftest import prepare_test_authenticated, BASE_URL
from aiowiserbyfeller import SmartButton, InvalidArgument


@pytest.mark.asyncio
async def test_async_get_smart_buttons(client_api_auth, mock_aioresponse):
    """Test async_get_smart_buttons."""
    response_json = {"status": "success", "data": [{"id": 2, "job": 6}]}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/smartbuttons", "get", response_json
    )

    actual = await client_api_auth.async_get_smart_buttons()

    assert len(actual) == 1
    assert isinstance(actual[0], SmartButton)
    assert actual[0].id == 2
    assert actual[0].job == 6


@pytest.mark.asyncio
async def test_async_get_smart_button(client_api_auth, mock_aioresponse):
    """Test async_get_smart_button."""
    response_json = {
        "status": "success",
        "data": {
            "job": 11,
            "input_channel": 0,
            "device_addr": 125933,
            "device": "0001ebed",
            "id": 10,
            "input_type": 1,
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/smartbuttons/2", "get", response_json
    )

    actual = await client_api_auth.async_get_smart_button(2)

    assert isinstance(actual, SmartButton)
    assert actual.id == 10
    assert actual.job == 11


@pytest.mark.asyncio
async def test_async_update_smart_button(client_api_auth, mock_aioresponse):
    """Test async_update_smart_button."""
    response_json = {"status": "success", "data": {"id": 2, "job": 6}}
    request_json = {"id": 2, "job": 6}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/smartbuttons/2",
        "patch",
        response_json,
        request_json,
    )

    button = SmartButton({"id": 2, "job": 6}, client_api_auth)
    actual = await client_api_auth.async_update_smart_button(button)

    assert isinstance(actual, SmartButton)
    assert actual.id == 2
    assert actual.job == 6


@pytest.mark.asyncio
async def test_async_program_smart_buttons(client_api_auth, mock_aioresponse):
    """Test async_program_smart_buttons."""
    response_json = {
        "status": "success",
        "data": {
            "on": True,
            "timeout": 60,
            "button_type": "groupctrl",
            "owner": "user",
        },
    }
    request_json = {"on": True, "timeout": 60}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/smartbuttons/program",
        "post",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_program_smart_buttons(True, 60)
    assert actual == response_json["data"]

    request_json["button_type"] = "groupctrl"
    request_json["owner"] = "user"

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/smartbuttons/program",
        "post",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_program_smart_buttons(
        True, 60, button_type="groupctrl", owner="user"
    )
    assert actual == response_json["data"]

    expected = "Invalid value invalid. Valid values: scene, groupctrl"
    with pytest.raises(InvalidArgument, match=expected):
        await client_api_auth.async_program_smart_buttons(
            True, 60, button_type="invalid", owner="user"
        )

    expected = "Invalid value invalid. Valid values: all, user"
    with pytest.raises(InvalidArgument, match=expected):
        await client_api_auth.async_program_smart_buttons(
            True, 60, button_type="groupctrl", owner="invalid"
        )


@pytest.mark.asyncio
async def test_async_notify_smart_buttons(client_api_auth, mock_aioresponse):
    """Test async_notify_smart_buttons."""
    response_json = {"status": "success", "data": {"button": 9}}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/smartbuttons/notify", "get", response_json
    )

    actual = await client_api_auth.async_notify_smart_buttons()
    assert actual == 9


@pytest.mark.asyncio
async def test_smart_button_async_refresh(client_api_auth, mock_aioresponse):
    """Test SmartButton.async_refresh."""
    response_json = {
        "status": "success",
        "data": {
            "job": 11,
            "input_channel": 0,
            "device_addr": 125933,
            "device": "0001ebed",
            "id": 10,
            "input_type": 1,
        },
    }

    raw_data = {
        "job": 6,
        "input_channel": 0,
        "device_addr": 125933,
        "device": "0001ebed",
        "id": 10,
        "input_type": 1,
    }

    button = SmartButton(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/smartbuttons/10", "get", response_json
    )

    await button.async_refresh()

    assert button.id == 10
    assert button.job == 11
    assert button.device_addr == 125933
    assert button.device == "0001ebed"
    assert button.input_type == 1
    assert button.input_channel == 0
