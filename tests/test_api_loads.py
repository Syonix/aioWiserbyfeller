"""aiowiserbyfeller Api class loads tests."""

import pytest

from aiowiserbyfeller import DaliRgbw, DaliTw, Dim, Hvac, InvalidArgument, Motor, OnOff
from aiowiserbyfeller.const import KIND_LIGHT, KIND_VENETIAN_BLINDS
from aiowiserbyfeller.hvac import HvacChannelState

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


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
            {
                "id": 4,
                "name": "Heizungskanal  2",
                "controller": "Heizungskontroller 1",
                "room": 789,
                "type": "hvac",
                "sub_type": "",
                "device": "00000679",
                "channel": 1,
                "unused": False,
            },
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads", "get", response_json
    )

    actual = await client_api_auth.async_get_loads()
    assert len(actual) == 4
    assert isinstance(actual[0], Dim)
    assert isinstance(actual[1], OnOff)
    assert isinstance(actual[2], Motor)
    assert isinstance(actual[3], Hvac)
    assert actual[0].id == 1
    assert actual[0].name == "Deckenspots"


@pytest.mark.asyncio
async def test_async_get_used_loads(client_api_auth, mock_aioresponse):
    """Test async_get_used_loads."""
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
                "unused": True,
                "kind": 0,
            },
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads", "get", response_json
    )

    actual = await client_api_auth.async_get_used_loads()
    assert len(actual) == 1
    assert isinstance(actual[0], Dim)
    assert actual[0].id == 1
    assert actual[0].name == "Deckenspots"


@pytest.mark.asyncio
async def test_async_get_unused_loads(client_api_auth, mock_aioresponse):
    """Test async_get_unused_loads."""
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
                "unused": True,
                "kind": 0,
            },
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/loads", "get", response_json
    )

    actual = await client_api_auth.async_get_unused_loads()
    assert len(actual) == 1
    assert isinstance(actual[0], OnOff)
    assert actual[0].id == 2
    assert actual[0].name == "Esstisch Lampe"


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
    """Test OnOff switch methods."""
    response_json_on = {
        "status": "success",
        "data": {"id": 2, "ctrl": {"button": "on", "event": "click"}},
    }
    response_json_off = {
        "status": "success",
        "data": {"id": 2, "ctrl": {"button": "on", "event": "click"}},
    }
    request_json_on = {"button": "on", "event": "click"}
    request_json_off = {"button": "off", "event": "click"}

    load = OnOff({"id": 2}, client_api_auth.auth, raw_state={"bri": 0})

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/ctrl",
        "put",
        response_json_on,
        request_json_on,
    )

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/ctrl",
        "put",
        response_json_off,
        request_json_off,
    )

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/ctrl",
        "put",
        response_json_on,
        request_json_on,
    )

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/ctrl",
        "put",
        response_json_off,
        request_json_off,
    )

    await load.async_switch_on()
    await load.async_switch_off()
    await load.async_switch(True)
    await load.async_switch(False)
    # Note: When using ctrl endpoint, no new target state is returned.


@pytest.mark.asyncio
async def test_motor_async_set_level(client_api_auth, mock_aioresponse):
    """Test Motor.async_set_level."""
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
    await load.async_set_level(10000)
    assert load.state["level"] == 10000


@pytest.mark.asyncio
async def test_motor_async_set_tilt(client_api_auth, mock_aioresponse):
    """Test Motor.async_set_tilt."""
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
    await load.async_set_tilt(9)
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
    await load.async_stop()
    assert load.state["moving"] == "stop"


@pytest.mark.asyncio
async def test_dim_on_off(client_api_auth, mock_aioresponse):
    """Test Dim on/off methods."""
    response_json_on = {
        "status": "success",
        "data": {"id": 2, "ctrl": {"button": "on", "event": "click"}},
    }
    response_json_off = {
        "status": "success",
        "data": {"id": 2, "ctrl": {"button": "on", "event": "click"}},
    }
    request_json_on = {"button": "on", "event": "click"}
    request_json_off = {"button": "off", "event": "click"}

    load = Dim({"id": 2}, client_api_auth.auth, raw_state={"bri": 0})

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/ctrl",
        "put",
        response_json_on,
        request_json_on,
    )

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/ctrl",
        "put",
        response_json_off,
        request_json_off,
    )

    await load.async_switch_on()
    await load.async_switch_off()
    # Note: When using ctrl endpoint, no new target state is returned.


@pytest.mark.asyncio
async def test_dim_async_set_bri(client_api_auth, mock_aioresponse):
    """Test Dim.async_set_bri."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "target_state": {"bri": 10000}},
    }
    request_json = {"bri": 10000}

    load = Dim({"id": 2}, client_api_auth.auth)
    assert load.state_bri is None

    load = Dim({"id": 2}, client_api_auth.auth, raw_state={"bri": 0})

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json,
        request_json,
    )

    assert load.state_bri == 0
    await load.async_set_bri(10000)
    assert load.state_bri == 10000


@pytest.mark.asyncio
async def test_dali_tw_async_set_bri_ct(client_api_auth, mock_aioresponse):
    """Test DaliTw.async_set_bri_ct."""
    response_json = {
        "status": "success",
        "data": {"id": 2, "target_state": {"bri": 10000, "ct": 20000}},
    }
    request_json = {"bri": 10000, "ct": 20000}

    load = DaliTw({"id": 2}, client_api_auth.auth)
    assert load.state is None
    assert load.state_ct is None

    load = DaliTw({"id": 2}, client_api_auth.auth, raw_state={"bri": 0, "ct": 1000})

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json,
        request_json,
    )

    assert load.state["ct"] == 1000
    await load.async_set_bri_ct(10000, 20000)
    assert load.state["ct"] == 20000
    assert load.state_ct == 20000


@pytest.mark.asyncio
async def test_dali_rgbw_async_set_bri_rgbw(client_api_auth, mock_aioresponse):
    """Test DaliRgbw.async_set_bri_rgbw."""
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

    load = DaliRgbw({"id": 2}, client_api_auth.auth)
    assert load.state_rgbw is None

    state = {"bri": 10000, "red": 0, "green": 0, "blue": 0, "white": 255}
    load = DaliRgbw({"id": 2}, client_api_auth.auth, raw_state=state)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/loads/2/target_state",
        "put",
        response_json,
        request_json,
    )

    await load.async_set_bri_rgbw(10000, 255, 0, 0, 0)
    assert load.state["red"] == 255
    assert load.state["white"] == 0
    assert load.state_rgbw == {"red": 255, "green": 0, "blue": 0, "white": 0}


@pytest.mark.asyncio
async def test_hvac(client_api_auth, mock_aioresponse):
    """Test heating channel properties."""
    state = {
        "heating_cooling_level": 0,
        "flags": {
            "remote_controlled": 0,
            "sensor_error": 0,
            "valve_error": 0,
            "noise": 0,
            "output_on": 1,
            "cooling": 0,
        },
        "target_temperature": 21,
        "boost_temperature": 0,
        "ambient_temperature": 25.1,
        "unit": "C",
    }

    # Empty data
    load = Hvac({}, client_api_auth.auth)
    load.raw_data = None
    assert load.controller is None
    assert load.heating_cooling_level is None
    assert load.target_temperature is None
    assert load.boost_temperature is None
    assert load.ambient_temperature is None
    assert load.unit is None
    assert load.flags == {}
    assert load.state == HvacChannelState.UNKNOWN
    assert load.state_heating is None
    assert load.state_cooling is None

    # Real data
    load = Hvac(
        {"id": 2, "controller": "Heating controller 1"},
        client_api_auth.auth,
        raw_state=state,
    )

    assert load.controller == "Heating controller 1"
    assert load.heating_cooling_level == 0
    assert load.target_temperature == 21.0
    assert load.boost_temperature == 0
    assert load.ambient_temperature == 25.1
    assert load.unit == "°C"
    assert load.flags == {
        "remote_controlled": False,
        "sensor_error": False,
        "valve_error": False,
        "noise": False,
        "output_on": True,
        "cooling": False,
    }
    assert load.flag("output_on") is True
    assert load.flag("this_flag_does_not_exist") is None

    assert load.state_heating is True
    assert load.state_cooling is False
    assert load.state == HvacChannelState.HEATING

    load.raw_state["flags"]["cooling"] = True
    assert load.state_heating is False
    assert load.state_cooling is True
    assert load.state == HvacChannelState.COOLING

    load.raw_state["flags"]["output_on"] = False
    load.raw_state["flags"]["cooling"] = False
    assert load.state_heating is False
    assert load.state_cooling is False
    assert load.state == HvacChannelState.IDLE

    load.raw_state["boost_temperature"] = -99
    assert load.state_heating is False
    assert load.state_cooling is False
    assert load.state == HvacChannelState.OFF
