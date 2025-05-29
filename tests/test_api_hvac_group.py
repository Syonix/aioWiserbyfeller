"""aiowiserbyfeller Api class HVAC group tests."""

import json
from pathlib import Path

import pytest

from aiowiserbyfeller import UnsuccessfulRequest
from aiowiserbyfeller.errors import InvalidState
from aiowiserbyfeller.hvac import HvacChannelState, HvacGroup
from aiowiserbyfeller.hvac.hvac import ThermostatReference

from .conftest import (  # noqa: TID251
    BASE_DATA_PATH,
    BASE_URL,
    prepare_test_authenticated,
)


@pytest.mark.asyncio
async def test_async_get_hvac_groups(client_api_auth, mock_aioresponse):
    """Test async_get_hvac_groups."""
    response_json = {
        "status": "success",
        "data": [],
    }

    with Path(BASE_DATA_PATH + "/valid/hvac_group.json").open("r") as f:  # noqa: ASYNC230
        response_json["data"].append(json.load(f))
    with Path(BASE_DATA_PATH + "/valid/hvac_group_without_thermostat_ref.json").open(  # noqa: ASYNC230
        "r"
    ) as f:
        response_json["data"].append(json.load(f))

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups", "get", response_json
    )

    actual = await client_api_auth.async_get_hvac_groups()

    assert len(actual) == 2
    assert isinstance(actual[0], HvacGroup)
    assert actual[0].id == 25
    assert actual[0].loads == [1]
    assert actual[0].name == "Office Heating Zone"
    assert actual[0].max_temperature == 25
    assert actual[0].min_temperature == 15
    assert actual[0].offset_temperature == 0
    assert actual[0].raw_state is None
    assert actual[0].state is HvacChannelState.UNKNOWN

    assert isinstance(actual[0].thermostat_ref, ThermostatReference)
    assert actual[0].thermostat_ref.input_type == 17
    assert actual[0].thermostat_ref.input_channel == 0
    assert actual[0].thermostat_ref.address == "0x00037797"

    assert actual[0].flags == {}

    assert actual[1].thermostat_ref is None


@pytest.mark.asyncio
async def test_async_create_hvac_group(client_api_auth, mock_aioresponse):
    """Test async_create_hvac_group."""
    with Path(BASE_DATA_PATH + "/valid/hvac_group.json").open("r") as f:  # noqa: ASYNC230
        response_json = {
            "status": "success",
            "data": json.load(f),
        }

    raw_data = {
        "loads": [1],
        "name": "Office Heating Zone",
        "max_temperature": 25,
        "min_temperature": 15,
        "offset_temperature": 0,
        "thermostat_ref": {
            "input_type": 17,
            "input_channel": 0,
            "address": "0x00037797",
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups", "post", response_json, raw_data
    )

    actual = await client_api_auth.async_create_hvac_group(
        HvacGroup(raw_data, client_api_auth.auth)
    )

    assert actual.id == 25
    assert actual.name == "Office Heating Zone"


@pytest.mark.asyncio
async def test_async_get_hvac_group(client_api_auth, mock_aioresponse):
    """Test async_get_hvac_group."""
    with Path(BASE_DATA_PATH + "/valid/hvac_group_with_state.json").open("r") as f:  # noqa: ASYNC230
        response_json = {
            "status": "success",
            "data": json.load(f),
        }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/27", "get", response_json
    )

    actual = await client_api_auth.async_get_hvac_group(27)

    assert isinstance(actual, HvacGroup)
    assert actual.id == 27
    assert actual.name == "Living Room Heating Zone"
    assert actual.is_on is True
    assert actual.state == HvacChannelState.HEATING
    assert actual.unit == "°C"


@pytest.mark.asyncio
async def test_async_get_hvac_group_states(client_api_auth, mock_aioresponse):
    """Test async_get_hvac_group_states."""
    with Path(BASE_DATA_PATH + "/valid/hvac_group_with_state.json").open("r") as f:  # noqa: ASYNC230
        group = json.load(f)
        response_json = {
            "status": "success",
            "data": [{"id": group["id"], "state": group["state"]}],
        }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/state", "get", response_json
    )

    actual = await client_api_auth.async_get_hvac_group_states()

    assert len(actual) == 1
    assert actual[0]["id"] == 27
    assert actual[0]["state"]["on"] is True
    assert actual[0]["state"]["ambient_temperature"] == 23.2


@pytest.mark.asyncio
async def test_async_refresh(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_refresh."""

    with Path(BASE_DATA_PATH + "/valid/hvac_group_with_state.json").open("r") as f:  # noqa: ASYNC230
        raw_data = json.load(f)

    response_json = {
        "status": "success",
        "data": {**raw_data, "loads": [1, 2]},
    }

    group = HvacGroup(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/27", "get", response_json
    )

    assert group.loads == [2]

    await group.async_refresh()

    assert group.loads == [1, 2]


@pytest.mark.asyncio
async def test_async_refresh_state(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_refresh_state."""

    with Path(BASE_DATA_PATH + "/valid/hvac_group.json").open("r") as f:  # noqa: ASYNC230
        raw_data = json.load(f)
    with Path(BASE_DATA_PATH + "/valid/hvac_group_with_state.json").open("r") as f:  # noqa: ASYNC230
        raw_data_state = json.load(f)

    response_json = {
        "status": "success",
        "data": raw_data_state,
    }

    group = HvacGroup(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/25", "get", response_json
    )

    await group.async_refresh_state()

    assert group.state == HvacChannelState.HEATING


@pytest.mark.asyncio
async def test_async_set_target_state(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_set_target_state."""

    with Path(BASE_DATA_PATH + "/valid/hvac_group_with_state.json").open("r") as f:  # noqa: ASYNC230
        raw_data = json.load(f)

    request_json = {"on": False, "target_temperature": 21.5}

    response_json = {
        "status": "success",
        "data": {
            **raw_data,
            "state": {**raw_data["state"], "on": False, "target_temperature": 21.5},
        },
    }

    group = HvacGroup(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/hvacgroups/27/target_state",
        "put",
        response_json,
        request_json,
    )

    await group.async_set_target_state({"on": False, "target_temperature": 21.5})

    assert group.is_on is False
    assert group.target_temperature == 21.5


@pytest.mark.asyncio
async def test_async_set_target_temperature(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_set_target_temperature."""

    with Path(BASE_DATA_PATH + "/valid/hvac_group_with_state.json").open("r") as f:  # noqa: ASYNC230
        raw_data = json.load(f)

    response_json = {
        "status": "success",
        "data": {
            **raw_data,
            "state": {**raw_data["state"], "target_temperature": 25.5},
        },
    }

    group = HvacGroup(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/hvacgroups/27/target_state",
        "put",
        response_json,
        {"target_temperature": 25.5},
    )

    await group.async_set_target_temperature(25.5)

    assert group.target_temperature == 25.5


@pytest.mark.asyncio
async def test_async_enable(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_enable."""

    with Path(BASE_DATA_PATH + "/valid/hvac_group_with_state.json").open("r") as f:  # noqa: ASYNC230
        raw_data = json.load(f)

    response_json = {
        "status": "success",
        "data": {**raw_data, "state": {**raw_data["state"], "on": False}},
    }

    group = HvacGroup(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/hvacgroups/27/target_state",
        "put",
        response_json,
        {"on": False},
    )

    await group.async_disable()

    assert group.is_on is False

    response_json["data"]["state"]["on"] = True
    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/hvacgroups/27/target_state",
        "put",
        response_json,
        {"on": True},
    )

    await group.async_enable()

    assert group.is_on is True


@pytest.mark.asyncio
async def test_async_replace_loads(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_replace_loads."""

    with Path(BASE_DATA_PATH + "/valid/hvac_group.json").open("r") as f:  # noqa: ASYNC230
        raw_data = json.load(f)

    request_json = {"loads": [2, 3]}

    response_json = {
        "status": "success",
        "data": {**raw_data, "loads": [2, 3]},
    }

    group = HvacGroup(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/hvacgroups/25",
        "put",
        response_json,
        request_json,
    )

    await group.async_replace_loads([2, 3])

    assert group.loads == [2, 3]


@pytest.mark.asyncio
async def test_async_append_loads(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_append_loads."""

    with Path(BASE_DATA_PATH + "/valid/hvac_group.json").open("r") as f:  # noqa: ASYNC230
        raw_data = json.load(f)

    request_json = {"loads": [2, 3]}

    response_json = {
        "status": "success",
        "data": {**raw_data, "loads": [1, 2, 3]},
    }

    group = HvacGroup(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/hvacgroups/25",
        "patch",
        response_json,
        request_json,
    )

    await group.async_append_loads([2, 3])

    assert group.loads == [1, 2, 3]


@pytest.mark.asyncio
async def test_async_delete_hvac_group(client_api_auth, mock_aioresponse):
    """Test async_delete_hvac_group."""

    with Path(BASE_DATA_PATH + "/valid/hvac_group.json").open("r") as f:  # noqa: ASYNC230
        raw_data = json.load(f)

    response_json = {
        "status": "success",
        "data": raw_data,
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/25", "delete", response_json
    )

    await client_api_auth.async_delete_hvac_group(25)


@pytest.mark.asyncio
async def test_async_get_binding_state(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_get_binding_state."""

    response_json = {
        "status": "success",
        "data": {"running": True},
    }

    group = HvacGroup({"id": 25}, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/25/bind", "get", response_json
    )

    assert await group.async_get_binding_state() is True


@pytest.mark.asyncio
async def test_async_stop_binding(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_stop_binding."""

    response_json = {
        "status": "success",
        "data": {"running": False},
    }

    request_json = {"running": False}

    group = HvacGroup({"id": 25}, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/hvacgroups/25/bind",
        "put",
        response_json,
        request_json,
    )

    assert await group.async_stop_binding() is True


@pytest.mark.asyncio
async def test_async_bind_thermostat_error(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_bind_thermostat with error."""

    response_json = {
        "status": "error",
        "message": "already bound",
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/25/bind", "patch", response_json
    )

    group = HvacGroup({"id": 25}, client_api_auth.auth)

    with pytest.raises(UnsuccessfulRequest, match="already bound"):
        await group.async_bind_thermostat()


@pytest.mark.asyncio
async def test_async_bind_thermostat(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_bind_thermostat."""
    with Path(BASE_DATA_PATH + "/valid/hvac_group.json").open("r") as f:  # noqa: ASYNC230
        response_json = {"status": "success", "data": json.load(f)}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/25/bind", "patch", response_json
    )

    group = HvacGroup({"id": 25}, client_api_auth.auth)

    assert group.thermostat_ref is None

    await group.async_bind_thermostat()

    assert isinstance(group.thermostat_ref, ThermostatReference)
    assert group.thermostat_ref.address == "0x00037797"


@pytest.mark.asyncio
async def test_async_delete_thermostat_binding(client_api_auth, mock_aioresponse):
    """Test HvacGroup.async_delete_thermostat_binding."""
    with Path(BASE_DATA_PATH + "/valid/hvac_group.json").open("r") as f:  # noqa: ASYNC230
        raw_data = json.load(f)
    with Path(BASE_DATA_PATH + "/valid/hvac_group_without_thermostat_ref.json").open(  # noqa: ASYNC230
        "r"
    ) as f:
        response_json = {"status": "success", "data": json.load(f)}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/25/bind", "delete", response_json
    )

    group = HvacGroup(raw_data, client_api_auth.auth)

    assert isinstance(group.thermostat_ref, ThermostatReference)
    assert group.thermostat_ref.address == "0x00037797"

    await group.async_delete_thermostat_binding()

    assert group.thermostat_ref is None


@pytest.mark.asyncio
async def test_async_bind_errors(client_api_auth, mock_aioresponse):
    """Test HvacGroup bind methods with missing id."""
    raw_data = {
        "loads": [1],
        "name": "Office Heating Zone",
        "max_temperature": 25,
        "min_temperature": 15,
        "offset_temperature": 0,
    }

    group = HvacGroup(raw_data, client_api_auth)

    with pytest.raises(
        InvalidState,
        match="Attempting to check binding status for HvacGroup instance without id.",
    ):
        await group.async_get_binding_state()

    with pytest.raises(
        InvalidState,
        match="Attempting to stop binding for HvacGroup instance without id.",
    ):
        await group.async_stop_binding()

    with pytest.raises(
        InvalidState,
        match="Attempting to binding thermostat to HvacGroup instance without id.",
    ):
        await group.async_bind_thermostat()

    with pytest.raises(
        InvalidState,
        match="Attempting to delete thermostat binding for HvacGroup instance without id.",
    ):
        await group.async_delete_thermostat_binding()


@pytest.mark.asyncio
async def test_async_create_hvac_group_config(client_api_auth, mock_aioresponse):
    """Test async_create_hvac_group_config."""
    with Path(BASE_DATA_PATH + "/valid/hvac_group_config.json").open("r") as f:  # noqa: ASYNC230
        response_json = {"status": "success", "data": json.load(f)}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/hvacgroups/25/config",
        "get",
        response_json,
    )

    actual = await client_api_auth.async_create_hvac_group_config(25)

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_hvac_group_config(client_api_auth, mock_aioresponse):
    """Test async_get_hvac_group_config."""
    with Path(BASE_DATA_PATH + "/valid/hvac_group_config.json").open("r") as f:  # noqa: ASYNC230
        response_json = {"status": "success", "data": json.load(f)}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/hvacgroups/configs/34",
        "get",
        response_json,
    )

    actual = await client_api_auth.async_get_hvac_group_config(34)

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_update_hvac_group_config(client_api_auth, mock_aioresponse):
    """Test async_update_hvac_group_config."""
    with Path(BASE_DATA_PATH + "/valid/hvac_group_config.json").open("r") as f:  # noqa: ASYNC230
        response_json = {"status": "success", "data": json.load(f)}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/hvacgroups/configs/34",
        "patch",
        response_json,
        {"min_temperature": 15},
    )

    actual = await client_api_auth.async_update_hvac_group_config(
        34, {"min_temperature": 15}
    )

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_apply_hvac_group_config(client_api_auth, mock_aioresponse):
    """Test async_apply_hvac_group_config."""
    with Path(BASE_DATA_PATH + "/valid/hvac_group_config.json").open("r") as f:  # noqa: ASYNC230
        response_json = {"status": "success", "data": json.load(f)}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/configs/34", "put", response_json
    )

    actual = await client_api_auth.async_apply_hvac_group_config(34)

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_discard_hvac_group_config(client_api_auth, mock_aioresponse):
    """Test async_discard_hvac_group_config."""
    with Path(BASE_DATA_PATH + "/valid/hvac_group_config.json").open("r") as f:  # noqa: ASYNC230
        response_json = {"status": "success", "data": json.load(f)}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/hvacgroups/configs/34", "delete", response_json
    )

    await client_api_auth.async_discard_hvac_group_config(34)
