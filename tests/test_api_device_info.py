"""aiowiserbyfeller Api class device info tests."""

import pytest

from .conftest import BASE_URL  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_info(client_api, mock_aioresponse):
    """Test get_info request."""
    response_json = {
        "status": "success",
        "data": {
            "product": "9020.001.002",
            "instance_id": 1800,
            "sn": "19100018",
            "api": "2.0",
            "sw": "2.0.0",
            "boot": "1.3.0",
            "hw": "2",
        },
    }

    mock_aioresponse.get(f"{BASE_URL}/info", payload=response_json)

    actual = await client_api.async_get_info()

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_info_debug(client_api, mock_aioresponse):
    """Test get_info_debug."""
    response_json = {
        "status": "success",
        "data": {
            "product": "9020.001.002",
            "instance_id": 1800,
            "sn": "19100018",
            "api": "2.0",
            "sw": "2.0.0",
            "sw_git": "09bae09-dirty",
            "sw_build": "2019-02-17T12:21:27",
            "mpy": "1.10.0",
            "mpy_git": "7ef9482b8",
            "boot": "1.3.0",
            "hw": "2",
            "wlan": "5.7.1",
            "wlan_build": "2019-02-11T17:04:09",
        },
    }

    mock_aioresponse.get(f"{BASE_URL}/info/debug", payload=response_json)

    actual = await client_api.async_get_info_debug()

    assert actual == response_json["data"]
