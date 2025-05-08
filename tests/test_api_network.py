"""aiowiserbyfeller Api class network tests."""

import pytest

from aiowiserbyfeller import InvalidArgument

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_net_scan(client_api_auth, mock_aioresponse):
    """Test async_get_net_scan."""
    response_json = {
        "status": "success",
        "data": [
            {
                "channel": 6,
                "ssid": "zApp-TestNet1",
                "sec": "WPA2",
                "bssid": "aa:9d:d3:10:34:b2",
                "rssi": -51,
            },
            {
                "channel": 11,
                "ssid": "VeryOldNet",
                "sec": "WEP",
                "bssid": "77:67:51:5f:87:b2",
                "rssi": -72,
            },
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/scan", "GET", response_json
    )

    actual = await client_api_auth.async_get_net_scan()
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_broadcast_net_mdns(client_api_auth, mock_aioresponse):
    """Test async_get_net_mdns and async_broadcast_net_mdns."""
    response_json = {
        "status": "success",
        "data": {
            "lisa": {
                "wiser-20012161": "192.168.1.155:80",
                "wiser-20023254": "192.168.1.87:80",
            },
            "zapp": {
                "zapp-17210151": "192.168.1.18:80",
                "zapp-17220047": "192.168.1.17:80",
                "zapp-20012161": "192.168.1.155:80",
                "zapp-20023254": "192.168.1.87:80",
            },
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/mdns", "GET", response_json
    )

    actual = await client_api_auth.async_get_net_mdns()
    assert actual == response_json["data"]

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/net/mdns",
        "POST",
        response_json,
        {"service": "lisa"},
    )

    actual = await client_api_auth.async_broadcast_net_mdns("lisa")
    assert actual == response_json["data"]

    with pytest.raises(InvalidArgument, match="Invalid mdns service value"):
        await client_api_auth.async_broadcast_net_mdns("invalid")


@pytest.mark.asyncio
async def test_async_get_net_wlans(client_api_auth, mock_aioresponse):
    """Test async_get_net_wlans."""
    response_json = {
        "status": "success",
        "data": [
            {
                "id": 1,
                "password": "**********",
                "_confirmed": True,
                "ssid": "potato",
                "sec": "WPA2",
                "bssid": "",
            },
            {
                "id": 2,
                "password": "**********",
                "_confirmed": True,
                "ssid": "cucumber",
                "sec": "WPA2",
                "bssid": "",
            },
            {
                "id": 3,
                "password": "**********",
                "_confirmed": False,
                "ssid": "Weekly Special",
                "sec": "WPA2",
                "bssid": "",
            },
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/wlans", "GET", response_json
    )

    actual = await client_api_auth.async_get_net_wlans()
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_create_wlan_config(client_api_auth, mock_aioresponse):
    """Test async_get_create_wlan_config."""
    response_json = {
        "status": "success",
        "data": {
            "id": 1,
            "ssid": "Weekly Special",
            "bssid": "",
            "sec": "WPA2",
            "password": "********",
            "_confirmed": False,
        },
    }

    request_json = {"ssid": "Weekly Special", "sec": "WPA2", "password": "27605973"}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/wlans", "POST", response_json, request_json
    )

    actual = await client_api_auth.async_get_create_wlan_config(
        "Weekly Special", "WPA2", "27605973"
    )
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_delete_wlan_configs(client_api_auth, mock_aioresponse):
    """Test async_delete_wlan_configs."""
    response_json = {"status": "success", "data": None}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/wlans", "DELETE", response_json
    )

    actual = await client_api_auth.async_delete_wlan_configs()
    assert actual is None


@pytest.mark.asyncio
async def test_async_get_net_wlan(client_api_auth, mock_aioresponse):
    """Test async_get_net_wlan."""
    response_json = {
        "status": "success",
        "data": {
            "id": 1,
            "ssid": "Weekly Special",
            "bssid": "",
            "sec": "WPA2",
            "password": "********",
            "_confirmed": False,
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/wlans/1", "GET", response_json
    )

    actual = await client_api_auth.async_get_net_wlan(1)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_put_net_wlan(client_api_auth, mock_aioresponse):
    """Test async_put_net_wlan."""
    response_json = {
        "status": "success",
        "data": {
            "id": 1,
            "ssid": "Weekly Special",
            "bssid": "",
            "sec": "WPA2",
            "password": "********",
            "_confirmed": False,
        },
    }

    request_json = {"ssid": "Weekly Special", "bssid": "77:67:51:5f:87:b2"}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/wlans/1", "put", response_json, request_json
    )

    actual = await client_api_auth.async_update_net_wlan(1, request_json)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_delete_net_wlan(client_api_auth, mock_aioresponse):
    """Test async_delete_net_wlan."""
    response_json = {
        "status": "success",
        "data": {
            "id": 1,
            "ssid": "Weekly Special",
            "bssid": "",
            "sec": "WPA2",
            "password": "********",
            "_confirmed": False,
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/wlans/1", "delete", response_json
    )

    actual = await client_api_auth.async_delete_net_wlan(1)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_net_state(client_api_auth, mock_aioresponse):
    """Test async_get_net_state."""
    response_json = {
        "status": "success",
        "data": {
            "hostname": "wiser-19021304",
            "ip": "192.168.7.244",
            "cloud_cn": "1800.devices.feller.ch",
            "current": 1,
            "https": False,
            "order": [1, 2],
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/state", "get", response_json
    )

    actual = await client_api_auth.async_get_net_state()
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_set_net_state(client_api_auth, mock_aioresponse):
    """Test async_set_net_state."""
    response_json = {
        "status": "success",
        "data": {
            "hostname": "wiser-19021304",
            "ip": "192.168.7.244",
            "cloud_cn": "1800.devices.feller.ch",
            "current": 1,
            "https": False,
            "order": [3, 1, 4],
        },
    }

    request_json = {"https": False, "order": [3, 1, 4]}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/state", "put", response_json, request_json
    )

    actual = await client_api_auth.async_set_net_state(request_json)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_update_net_state(client_api_auth, mock_aioresponse):
    """Test async_update_net_state."""
    response_json = {
        "status": "success",
        "data": {
            "hostname": "wiser-19021304",
            "ip": "192.168.7.244",
            "cloud_cn": "1800.devices.feller.ch",
            "current": 1,
            "https": False,
            "order": [3, 1, 4],
        },
    }

    request_json = {"https": False, "order": [3, 1, 4]}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/state", "patch", response_json, request_json
    )

    actual = await client_api_auth.async_update_net_state(request_json)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_net_rssi(client_api_auth, mock_aioresponse):
    """Test async_get_net_rssi."""
    response_json = {"status": "success", "data": {"rssi": -69}}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/net/rssi", "get", response_json
    )

    actual = await client_api_auth.async_get_net_rssi()
    assert actual == response_json["data"]["rssi"]
