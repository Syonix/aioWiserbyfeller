"""aiowiserbyfeller Api class device tests."""

import pytest

from aiowiserbyfeller import Device

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_devices(client_api_auth, mock_aioresponse):
    """Test async_get_devices."""
    response_json = {
        "status": "success",
        "data": [
            {
                "id": "00000679",
                "last_seen": 25,
                "a": {
                    "fw_id": "0x0200",
                    "hw_id": "0x1202",
                    "fw_version": "0x00500a28",
                    "address": "0x00004103",
                    "comm_ref": "3406.A",
                },
                "c": {
                    "fw_id": "0x8402",
                    "hw_id": "0x8443",
                    "fw_version": "0x00500a28",
                    "cmd_matrix": "0x0002",
                    "comm_ref": "926-3406-4.S4.A.F",
                },
            },
            {
                "id": "000004d7",
                "last_seen": 6,
                "a": {
                    "fw_id": "0x0100",
                    "hw_id": "0x1110",
                    "fw_version": "0x00501a30",
                    "address": "0x00000af6",
                    "comm_ref": "3404.A",
                },
                "c": {
                    "fw_id": "0x8402",
                    "hw_id": "0x8443",
                    "fw_version": "0x00500a28",
                    "cmd_matrix": "0x0002",
                    "comm_ref": "926-3406-4.S4.A.F",
                },
            },
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/devices", "get", response_json
    )

    actual = await client_api_auth.async_get_devices()

    assert len(actual) == 2
    assert isinstance(actual[0], Device)
    assert actual[0].id == "00000679"
    assert actual[0].last_seen == 25
    assert actual[0].a == response_json["data"][0]["a"]
    assert actual[0].c == response_json["data"][0]["c"]


@pytest.mark.asyncio
async def test_async_get_devices_detail(client_api_auth, mock_aioresponse):
    """Test async_get_devices_detail."""
    response_json = {
        "status": "success",
        "data": [
            {
                "id": "000006d7",
                "last_seen": 39,
                "a": {
                    "fw_id": "0x0100",
                    "hw_id": "0x1110",
                    "fw_version": "0x00501a30",
                    "comm_ref": "3401A",
                    "address": "0x00000679",
                    "nubes_id": 4294967294,
                    "comm_name": "Druckschalter 1K",
                    "serial_nr": "011110_B_000064",
                },
                "c": {
                    "fw_id": "0x8402",
                    "hw_id": "0x8443",
                    "fw_version": "0x00500a28",
                    "comm_ref": "926-3406.4.S.A.F",
                    "cmd_matrix": "0x0002",
                    "nubes_id": 999,
                    "comm_name": "Druckschalter 1K Sz",
                    "serial_nr": "018443_B_000050",
                },
                "inputs": [{"type": "up down"}],
                "outputs": [{"load": 6, "type": "motor", "sub_type": ""}],
            }
        ],
    }

    mock_aioresponse.get(f"{BASE_URL}/devices/*", payload=response_json)

    actual = await client_api_auth.async_get_devices_detail()

    assert len(actual) == 1
    assert isinstance(actual[0], Device)
    assert actual[0].id == "000006d7"
    assert actual[0].last_seen == 39
    assert actual[0].a == response_json["data"][0]["a"]
    assert actual[0].inputs == response_json["data"][0]["inputs"]
    assert actual[0].outputs == response_json["data"][0]["outputs"]

    c_sn = response_json["data"][0]["c"]["serial_nr"]
    a_sn = response_json["data"][0]["a"]["serial_nr"]
    assert actual[0].combined_serial_number == f"{c_sn} / {a_sn}"


@pytest.mark.asyncio
async def test_async_get_device(client_api_auth, mock_aioresponse):
    """Test async_get_device."""
    response_json = {
        "status": "success",
        "data": {
            "id": "000006d7",
            "last_seen": 39,
            "a": {
                "fw_id": "0x0100",
                "hw_id": "0x1110",
                "fw_version": "0x00501a30",
                "comm_ref": "3401A",
                "address": "0x00000679",
                "nubes_id": 4294967294,
                "comm_name": "Druckschalter 1K",
                "serial_nr": "011110_B_000064",
            },
            "c": {
                "fw_id": "0x8402",
                "hw_id": "0x8443",
                "fw_version": "0x00500a28",
                "comm_ref": "926-3406.4.S.A.F",
                "cmd_matrix": "0x0002",
                "nubes_id": 999,
                "comm_name": "Druckschalter 1K Sz",
                "serial_nr": "018443_B_000050",
            },
            "inputs": [{"type": "up down"}],
            "outputs": [{"load": 6, "type": "motor", "sub_type": ""}],
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/devices/000006d7", "get", response_json
    )

    actual = await client_api_auth.async_get_device("000006d7")

    assert isinstance(actual, Device)
    assert actual.id == "000006d7"
    assert actual.last_seen == 39
    assert actual.a == response_json["data"]["a"]
    assert actual.outputs == response_json["data"]["outputs"]


@pytest.mark.asyncio
async def test_async_delete_device(client_api_auth, mock_aioresponse):
    """Test async_delete_device."""
    response_json = {
        "status": "success",
        "data": {
            "id": "000006d7",
            "last_seen": 39,
            "a": {
                "fw_id": "0x0100",
                "hw_id": "0x1110",
                "fw_version": "0x00501a30",
                "comm_ref": "3401A",
                "address": "0x00000679",
                "nubes_id": 4294967294,
                "comm_name": "Druckschalter 1K",
                "serial_nr": "011110_B_000064",
            },
            "c": {
                "fw_id": "0x8402",
                "hw_id": "0x8443",
                "fw_version": "0x00500a28",
                "comm_ref": "926-3406.4.S.A.F",
                "cmd_matrix": "0x0002",
                "nubes_id": 999,
                "comm_name": "Druckschalter 1K Sz",
                "serial_nr": "018443_B_000050",
            },
            "inputs": [{"type": "up down"}],
            "outputs": [{"load": 6, "type": "motor", "sub_type": ""}],
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/devices/000006d7", "delete", response_json
    )

    actual = await client_api_auth.async_delete_device("000006d7")

    assert isinstance(actual, Device)
    assert actual.id == "000006d7"


@pytest.mark.asyncio
async def test_async_get_device_config(client_api_auth, mock_aioresponse):
    """Test async_get_device_config."""
    response_json = {
        "status": "success",
        "data": {
            "id": 4294976294,
            "inputs": [
                {
                    "type": "toggle",
                    "color": "#10f220",
                    "background_bri": 10,
                    "foreground_bri": 8,
                }
            ],
            "outputs": [
                {
                    "load": 301,
                    "type": "onoff",
                    "sub_type": "",
                    "delayed_off": False,
                    "delay_ms": 200,
                },
                {
                    "load": 302,
                    "type": "onoff",
                    "sub_type": "",
                    "delayed_off": False,
                    "delay_ms": 200,
                },
            ],
            "design": {"color": 0, "name": "edizio_due"},
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/devices/000006d7/config", "get", response_json
    )

    actual = await client_api_auth.async_get_device_config("000006d7")

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_device_input_config(client_api_auth, mock_aioresponse):
    """Test async_get_device_input_config."""
    response_json = {
        "status": "success",
        "data": {
            "status": "success",
            "data": {
                "type": "toggle",
                "color": "#10f220",
                "background_bri": 10,
                "foreground_bri": 8,
            },
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/config/4294976294/inputs/0",
        "get",
        response_json,
    )

    actual = await client_api_auth.async_get_device_input_config("4294976294", 0)

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_set_device_input_config(client_api_auth, mock_aioresponse):
    """Test async_set_device_input_config."""
    response_json = {
        "status": "success",
        "data": {
            "status": "success",
            "data": {
                "type": "toggle",
                "color": "#111111",
                "background_bri": 10,
                "foreground_bri": 8,
            },
        },
    }

    request_json = {"color": "#111111"}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/config/4294976294/inputs/0",
        "patch",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_set_device_input_config(
        "4294976294", 0, request_json
    )

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_device_output_config(client_api_auth, mock_aioresponse):
    """Test async_get_device_output_config."""
    response_json = {
        "status": "success",
        "data": {
            "load": 301,
            "type": "onoff",
            "sub_type": "",
            "delayed_off": False,
            "delay_ms": 200,
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/config/4294976294/inputs/0",
        "get",
        response_json,
    )

    actual = await client_api_auth.async_get_device_output_config("4294976294", 0)

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_set_device_output_config(client_api_auth, mock_aioresponse):
    """Test async_set_device_output_config."""
    response_json = {
        "status": "success",
        "data": {
            "load": 301,
            "type": "onoff",
            "sub_type": "",
            "delayed_off": False,
            "delay_ms": 200,
        },
    }

    request_json = {"delay_ms": 200}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/config/4294976294/outputs/0",
        "patch",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_set_device_output_config(
        "4294976294", 0, request_json
    )

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_device_config2(client_api_auth, mock_aioresponse):
    """Test async_get_device_config2."""
    response_json = {
        "status": "success",
        "data": {
            "id": 4294976294,
            "inputs": [
                {
                    "type": "toggle",
                    "color": "#10f220",
                    "background_bri": 10,
                    "foreground_bri": 8,
                }
            ],
            "outputs": [
                {
                    "load": 301,
                    "type": "onoff",
                    "sub_type": "",
                    "delayed_off": False,
                    "delay_ms": 200,
                },
                {
                    "load": 302,
                    "type": "onoff",
                    "sub_type": "",
                    "delayed_off": False,
                    "delay_ms": 200,
                },
            ],
            "design": {"color": 0, "name": "edizio_due"},
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/config/4294976294",
        "get",
        response_json,
    )

    actual = await client_api_auth.async_get_device_config_by_config_id("4294976294")

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_apply_device_config(client_api_auth, mock_aioresponse):
    """Test async_apply_device_config."""
    response_json = {
        "status": "success",
        "data": {
            "id": 4294976294,
            "inputs": [
                {
                    "type": "toggle",
                    "color": "#10f220",
                    "background_bri": 10,
                    "foreground_bri": 8,
                }
            ],
            "outputs": [
                {
                    "load": 301,
                    "type": "onoff",
                    "sub_type": "",
                    "delayed_off": False,
                    "delay_ms": 200,
                },
                {
                    "load": 302,
                    "type": "onoff",
                    "sub_type": "",
                    "delayed_off": False,
                    "delay_ms": 200,
                },
            ],
            "design": {"color": 0, "name": "edizio_due"},
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/config/4294976294",
        "put",
        response_json,
    )

    actual = await client_api_auth.async_apply_device_config("4294976294")

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_discard_device_config(client_api_auth, mock_aioresponse):
    """Test async_discard_device_config."""
    response_json = {
        "status": "success",
        "data": {
            "id": 4294976294,
            "inputs": [
                {
                    "type": "toggle",
                    "color": "#10f220",
                    "background_bri": 10,
                    "foreground_bri": 8,
                }
            ],
            "outputs": [
                {
                    "load": 301,
                    "type": "onoff",
                    "sub_type": "",
                    "delayed_off": False,
                    "delay_ms": 200,
                },
                {
                    "load": 302,
                    "type": "onoff",
                    "sub_type": "",
                    "delayed_off": False,
                    "delay_ms": 200,
                },
            ],
            "design": {"color": 0, "name": "edizio_due"},
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/config/4294976294",
        "delete",
        response_json,
    )

    actual = await client_api_auth.async_discard_device_config("4294976294")

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_find_device(client_api_auth, mock_aioresponse):
    """Test async_find_device."""
    response_json = {
        "status": "success",
        "data": {"device": "00002681", "channel": 1, "type": "scene"},
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/findme",
        "put",
        response_json,
    )

    actual = await client_api_auth.async_find_device()

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_devices_info(client_api_auth, mock_aioresponse):
    """Test async_get_devices_info."""
    response_json = {
        "status": "success",
        "data": {
            "max_last_seen": 780,
            "count": 8,
            "C_FWID": {"8402": {"count": 5, "fw_versions": ["10102906", "10106001"]}},
            "A_FWID": {"0100": {"count": 3, "fw_versions": ["20002b05", "20100001"]}},
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/info",
        "get",
        response_json,
    )

    actual = await client_api_auth.async_get_devices_info()

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_load_async_ping(client_api_auth, mock_aioresponse):
    """Test Load::async_ping."""
    response_json = {"status": "success", "data": {"ping": "pong"}}

    raw_data = {
        "id": "00000679",
        "last_seen": 25,
        "a": {
            "fw_id": "0x0200",
            "hw_id": "0x1202",
            "fw_version": "0x00500a28",
            "address": "0x00004103",
            "comm_ref": "3406.A",
        },
        "c": {
            "fw_id": "0x8402",
            "hw_id": "0x8443",
            "fw_version": "0x00500a28",
            "cmd_matrix": "0x0002",
            "comm_ref": "926-3406-4.S4.A.F",
        },
    }

    device = Device(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/00000679/ping",
        "get",
        response_json,
    )

    actual = await device.async_ping()
    assert actual is True


@pytest.mark.asyncio
async def test_async_calibrate_motor_devices(client_api_auth, mock_aioresponse):
    """Test async_calibrate_motor_devices."""
    response_json = {"status": "success", "data": None}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/motor/calibration",
        "put",
        response_json,
    )

    actual = await client_api_auth.async_calibrate_motor_devices()

    assert actual == response_json["data"]


@pytest.mark.parametrize(
    ("foreground_param", "foreground_expected"), [(None, 100), (50, 50)]
)
@pytest.mark.asyncio
async def test_async_status(
    client_api_auth,
    mock_aioresponse,
    foreground_param: int | None,
    foreground_expected: int,
):
    """Test async_status."""

    raw_data = {
        "id": "00000679",
        "last_seen": 25,
        "a": {
            "fw_id": "0x0200",
            "hw_id": "0x1202",
            "fw_version": "0x00500a28",
            "address": "0x00004103",
            "comm_ref": "3406.A",
        },
        "c": {
            "fw_id": "0x8402",
            "hw_id": "0x8443",
            "fw_version": "0x00500a28",
            "cmd_matrix": "0x0002",
            "comm_ref": "926-3406-4.S4.A.F",
        },
    }

    config_response = {
        "status": "success",
        "data": {
            "id": 4294976294,
            "inputs": [
                {
                    "type": "toggle",
                    "color": "#10f220",
                    "background_bri": 10,
                    "foreground_bri": 8,
                }
            ],
            "outputs": [
                {
                    "load": 301,
                    "type": "onoff",
                    "sub_type": "",
                    "delayed_off": False,
                    "delay_ms": 200,
                }
            ],
            "design": {"color": 0, "name": "edizio_due"},
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/00000679/config",
        "get",
        config_response,
    )

    update_request = {
        "color": "#552030",
        "background_bri": 100,
        "foreground_bri": foreground_expected,
    }

    update_response = {
        "status": "success",
        "data": {
            "type": "toggle",
            "color": "#552030",
            "background_bri": 100,
            "foreground_bri": foreground_expected,
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/devices/config/4294976294/inputs/0",
        "put",
        update_response,
        update_request,
    )

    apply_response = config_response
    apply_response["data"]["inputs"][0]["color"] = "#552030"
    apply_response["data"]["inputs"][0]["background_bri"] = 100
    apply_response["data"]["inputs"][0]["foreground_bri"] = foreground_expected

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/devices/config/4294976294", "put", apply_response
    )

    device = Device(raw_data, client_api_auth.auth)
    await device.async_status(0, "#552030", 100, foreground_param)
