"""aiowiserbyfeller Api class loads tests"""
import pytest
from .conftest import prepare_test_authenticated, BASE_URL
from aiowiserbyfeller import (
    InvalidArgument,
    Dim,
    DaliTw,
    DaliRgbw,
    OnOff,
    Motor,
    KIND_VENETIAN_BLINDS,
    KIND_LIGHT,
)


@pytest.mark.asyncio
async def test_async_get_loads(client_api_auth, mock_aioresponse):
    """Test async_get_loads."""
    response_json = {
        "status": "success",
        "data": [
            {
                "id": 1,
                "name": "Deckenspots",
                "room": 123,
                "type": "dim",
                "sub_type": "",
                "device": "000004d7",
                "channel": 0,
                "unused": False,
                "kind": 0,
            },
            {
                "id": 2,
                "name": "Esstisch Lampe",
                "room": 456,
                "type": "onoff",
                "sub_type": "",
                "device": "000004d7",
                "channel": 1,
                "unused": False,
                "kind": 0,
            },
            {
                "id": 3,
                "name": "Fenster West",
                "room": 789,
                "type": "motor",
                "sub_type": "",
                "device": "00000679",
                "channel": 0,
                "unused": False,
                "kind": 0,
            },
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads", "get", response_json
    )

    actual = await client_api_auth.async_get_loads()
    assert len(actual) == 3
    assert isinstance(actual[0], Dim)
    assert isinstance(actual[1], OnOff)
    assert isinstance(actual[2], Motor)
    assert actual[0].id == 1
    assert actual[0].name == "Deckenspots"


@pytest.mark.asyncio
async def test_async_get_load(client_api_auth, mock_aioresponse):
    """Test async_get_load."""
    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "name": "Esstisch Lampe",
            "unused": False,
            "type": "dali",
            "sub_type": "tw",
            "device": "0000072d",
            "channel": 0,
            "room": 123,
            "kind": 0,
            "state": {"bri": 10000},
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads/2", "get", response_json
    )

    actual = await client_api_auth.async_get_load(2)
    assert isinstance(actual, DaliTw)
    assert actual.id == 2
    assert actual.name == "Esstisch Lampe"


@pytest.mark.asyncio
async def test_stateless_load(client_api_auth, mock_aioresponse):
    """Test Load.state."""
    raw_data = {
        "id": 2,
        "name": "Esstisch Lampe",
        "unused": False,
        "type": "dali",
        "sub_type": "tw",
        "device": "0000072d",
        "channel": 0,
        "room": 123,
        "kind": 0,
        "state": {"bri": 10000},
    }

    load = OnOff(raw_data, client_api_auth.auth)

    assert load.state is None


@pytest.mark.asyncio
async def test_async_update_load(client_api_auth, mock_aioresponse):
    """Test async_update_load."""
    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "name": "Esstisch Lampe",
            "unused": False,
            "type": "dali",
            "sub_type": "tw",
            "device": "0000072d",
            "channel": 0,
            "room": 123,
            "kind": 0,
            "state": {"bri": 10000},
        },
    }

    request_json = {
        "id": 2,
        "name": "Esstisch Lampe",
        "unused": False,
        "type": "dali",
        "sub_type": "tw",
        "device": "0000072d",
        "channel": 0,
        "room": 123,
        "kind": 0,
        "state": {"bri": 10000},
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads/2", "patch", response_json, request_json
    )

    load = DaliTw(request_json, client_api_auth)

    actual = await client_api_auth.async_update_load(load)
    assert actual.id == 2
    assert actual.name == "Esstisch Lampe"


@pytest.mark.asyncio
async def test_async_patch_load(client_api_auth, mock_aioresponse):
    """Test async_patch_load."""
    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "name": "Esstisch Lampe",
            "unused": False,
            "type": "dali",
            "sub_type": "tw",
            "device": "0000072d",
            "channel": 0,
            "room": 123,
            "kind": 0,
            "state": {"bri": 10000},
        },
    }

    request_json = {"name": "Esstisch Lampe", "room": 123}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads/2", "patch", response_json, request_json
    )

    actual = await client_api_auth.async_patch_load(2, request_json)
    assert actual["id"] == 2
    assert actual["name"] == "Esstisch Lampe"


@pytest.mark.asyncio
async def test_async_get_load_state(client_api_auth, mock_aioresponse):
    """Test async_get_load_state."""
    response_json = {"status": "success", "data": {"id": 2, "state": {"bri": 10000}}}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads/2/state", "get", response_json
    )

    actual = await client_api_auth.async_get_load_state(2)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_load_async_set_target_state(client_api_auth, mock_aioresponse):
    """Test Load::async_set_target_state."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "target_state": {"bri": 10000}},
    }

    raw_data = {
        "id": 2,
        "name": "Esstisch Lampe",
        "unused": False,
        "type": "dali",
        "sub_type": "tw",
        "device": "0000072d",
        "channel": 0,
        "room": 123,
        "kind": 0,
    }

    load = Dim(raw_data, client_api_auth.auth, raw_state={"bri": 0})
    request_json = {"bri": 10000}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json,
        request_json,
    )

    await load.async_set_target_state(request_json)
    assert load.raw_state == response_json["data"]["target_state"]


@pytest.mark.asyncio
async def test_load_async_ctrl(client_api_auth, mock_aioresponse):
    """Test Load::async_ctrl."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "ctrl": {"button": "up", "event": "click"}},
    }

    raw_data = {
        "id": 2,
        "name": "Esstisch Lampe",
        "unused": False,
        "type": "dali",
        "sub_type": "tw",
        "device": "0000072d",
        "channel": 0,
        "room": 123,
        "kind": 0,
    }

    load = Dim(raw_data, client_api_auth.auth, raw_state={"bri": 0})
    request_json = {"button": "up", "event": "click"}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/ctrl",
        "put",
        response_json,
        request_json,
    )

    await load.async_ctrl("up", "click")

    with pytest.raises(InvalidArgument, match="Invalid button value"):
        await load.async_ctrl("invalid", "click")

    with pytest.raises(InvalidArgument, match="Invalid button event value"):
        await load.async_ctrl("up", "invalid")


@pytest.mark.asyncio
async def test_load_async_ping(client_api_auth, mock_aioresponse):
    """Test Load::async_ping."""
    response_json = {
        "status": "success",
        "data": {"time_ms": 2000, "blink_pattern": "ramp", "color": "#505050"},
    }

    raw_data = {
        "id": 2,
        "name": "Esstisch Lampe",
        "unused": False,
        "type": "dali",
        "sub_type": "tw",
        "device": "0000072d",
        "channel": 0,
        "room": 123,
        "kind": 0,
    }

    load = Dim(raw_data, client_api_auth.auth, raw_state={"bri": 0})
    request_json = {"time_ms": 2000, "blink_pattern": "ramp", "color": "#505050"}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/ping",
        "put",
        response_json,
        request_json,
    )

    await load.async_ping(2000, "ramp", "#505050")


@pytest.mark.asyncio
async def test_async_find_loads(client_api_auth, mock_aioresponse):
    """Test async_find_loads."""
    response_json = {
        "status": "success",
        "data": {"on": True, "time": 2, "blink_pattern": "ramp", "color": "#505050"},
    }

    request_json = {"on": True, "time": 2, "blink_pattern": "ramp", "color": "#505050"}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads/findme", "put", response_json, request_json
    )

    actual = await client_api_auth.async_find_loads(True, 2, "ramp", "#505050")
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_load_async_refresh(client_api_auth, mock_aioresponse):
    """Test Load.async_refresh."""
    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "name": "Büro Lampe",
            "room": 45,
            "type": "onoff",
            "sub_type": "",
            "device": "000004d7",
            "channel": 0,
            "unused": False,
            "kind": 0,
        },
    }
    state_response_json = {
        "status": "success",
        "data": {"id": 2, "state": {"bri": 10000}},
    }

    raw_data = {
        "id": 2,
        "name": "Esstisch Lampe",
        "room": 456,
        "type": "onoff",
        "sub_type": "",
        "device": "000004d7",
        "channel": 1,
        "unused": False,
        "kind": 0,
    }

    load = OnOff(raw_data, client_api_auth.auth, raw_state={"bri": 0})

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads/2", "get", response_json
    )

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads/2/state", "get", state_response_json
    )

    await load.async_refresh()

    assert load.id == 2
    assert load.name == "Büro Lampe"
    assert load.room == 45
    assert load.type == "onoff"
    assert load.sub_type == ""
    assert load.device == "000004d7"
    assert load.channel == 0
    assert load.unused is False
    assert load.kind == KIND_LIGHT

    assert load.state is True


@pytest.mark.asyncio
async def test_on_off_async_control(client_api_auth, mock_aioresponse):
    """Test OnOff.async_control."""
    response_json_on = {
        "status": "success",
        "data": {"id": 2, "target_state": {"bri": 10000}},
    }
    response_json_off = {
        "status": "success",
        "data": {"id": 2, "target_state": {"bri": 0}},
    }
    request_json_on = {"bri": 10000}
    request_json_off = {"bri": 0}

    load = OnOff({"id": 2}, client_api_auth.auth, raw_state={"bri": 0})

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json_on,
        request_json_on,
    )

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json_off,
        request_json_off,
    )

    assert load.state is False
    await load.async_control_on()
    assert load.state is True
    await load.async_control_off()
    assert load.state is False


@pytest.mark.asyncio
async def test_motor_async_control_level(client_api_auth, mock_aioresponse):
    """Test Motor.async_control_level."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "target_state": {"level": 10000, "tilt": 0}},
    }
    request_json = {"level": 10000}

    load = Motor({"id": 2}, client_api_auth.auth)
    assert load.state is None

    load = Motor({"id": 2}, client_api_auth.auth, raw_state={"level": 0, "tilt": 0})

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json,
        request_json,
    )

    assert load.state["level"] == 0
    await load.async_control_level(10000)
    assert load.state["level"] == 10000


@pytest.mark.asyncio
async def test_motor_async_control_tilt(client_api_auth, mock_aioresponse):
    """Test Motor.async_control_tilt."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "target_state": {"level": 10000, "tilt": 9}},
    }
    request_json = {"tilt": 9}

    load = Motor({"id": 2}, client_api_auth.auth, raw_state={"level": 10000, "tilt": 0})

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json,
        request_json,
    )

    assert load.kind is None
    assert load.state["tilt"] == 0
    await load.async_control_tilt(9)
    assert load.state["tilt"] == 9


@pytest.mark.asyncio
async def test_motor_async_stop(client_api_auth, mock_aioresponse):
    """Test Motor.async_control_stop."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "target_state": {"moving": "stop"}},
    }
    request_json = {"button": "stop", "event": "click"}

    load = Motor(
        {"id": 2, "kind": 1},
        client_api_auth.auth,
        raw_state={
            "level": 10000,
            "moving": "down",
            "tilt": 0,
        },
    )

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/ctrl",
        "put",
        response_json,
        request_json,
    )

    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "state": {
                "level": 10000,
                "moving": "stop",
                "tilt": 0,
            },
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/state",
        "get",
        response_json,
    )

    assert load.kind == KIND_VENETIAN_BLINDS
    assert load.state["moving"] == "down"
    await load.async_control_stop()
    assert load.state["moving"] == "stop"


@pytest.mark.asyncio
async def test_dim_async_control_bri(client_api_auth, mock_aioresponse):
    """Test Dim.async_control_bri."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "target_state": {"bri": 10000}},
    }
    request_json = {"bri": 10000}

    load = Dim({"id": 2}, client_api_auth.auth)
    assert load.state is None

    load = Dim({"id": 2}, client_api_auth.auth, raw_state={"bri": 0})

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json,
        request_json,
    )

    assert load.state == 0
    await load.async_control_bri(10000)
    assert load.state == 10000


@pytest.mark.asyncio
async def test_dali_tw_async_control_bri(client_api_auth, mock_aioresponse):
    """Test DaliTw.async_control_bri."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "target_state": {"bri": 10000, "ct": 20000}},
    }
    request_json = {"bri": 10000, "ct": 20000}

    load = DaliTw({"id": 2}, client_api_auth.auth)
    assert load.state is None

    load = DaliTw({"id": 2}, client_api_auth.auth, raw_state={"bri": 0, "ct": 1000})

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json,
        request_json,
    )

    assert load.state["ct"] == 1000
    await load.async_control_bri(10000, 20000)
    assert load.state["ct"] == 20000


@pytest.mark.asyncio
async def test_dali_rgbw_async_control_bri(client_api_auth, mock_aioresponse):
    """Test DaliRgbw.async_control_bri."""
    response_json = {
        "status": "success",
        "data": {
            "id": 2,
            "target_state": {
                "bri": 10000,
                "red": 255,
                "green": 0,
                "blue": 0,
                "white": 0,
            },
        },
    }
    request_json = {"bri": 10000, "red": 255, "green": 0, "blue": 0, "white": 0}

    state = {"bri": 10000, "red": 0, "green": 0, "blue": 0, "white": 255}
    load = DaliRgbw({"id": 2}, client_api_auth.auth, raw_state=state)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json,
        request_json,
    )

    await load.async_control_bri(10000, 255, 0, 0, 0)
    assert load.state["red"] == 255
    assert load.state["white"] == 0
