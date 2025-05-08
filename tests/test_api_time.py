"""aiowiserbyfeller Api class time tests."""

import pytest

from aiowiserbyfeller import NtpConfig

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_set_time_now(client_api_auth, mock_aioresponse):
    """Test async_get_time_now and async_set_time_now."""
    response_json = {
        "status": "success",
        "data": {
            "utc": "2019-02-05T13:03:55",
            "local": "2019-02-05T14:03:55",
            "uptime": 277,
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/time/now", "GET", response_json
    )

    actual = await client_api_auth.async_get_time_now()
    assert actual == response_json["data"]

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/time/now",
        "PUT",
        response_json,
        {"utc": "2019-02-05T13:03:55"},
    )

    actual = await client_api_auth.async_set_time_now("2019-02-05T13:03:55")
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_ntpconfig(client_api_auth, mock_aioresponse):
    """Test async_get_ntpconfig."""
    response_json = {
        "status": "success",
        "data": {"interval": 12, "urls": ["192.168.0.1", "ch.pool.ntp.org"]},
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/time/ntpconfig", "GET", response_json
    )

    actual = await client_api_auth.async_get_time_ntp_config()
    assert isinstance(actual, NtpConfig)
    assert actual.interval == 12
    assert actual.urls == ["192.168.0.1", "ch.pool.ntp.org"]


@pytest.mark.asyncio
async def test_async_set_ntpconfig(client_api_auth, mock_aioresponse):
    """Test async_set_ntpconfig."""
    response_json = {
        "status": "success",
        "data": {"interval": 72, "urls": ["ntp.metas.ch"]},
    }
    request_json = {"interval": 72, "urls": ["ntp.metas.ch"]}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/time/ntpconfig",
        "PUT",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_set_time_ntp_config(72, ["ntp.metas.ch"])
    assert actual.interval == 72


@pytest.mark.asyncio
async def test_async_patch_ntpconfig(client_api_auth, mock_aioresponse):
    """Test async_patch_ntpconfig."""
    response_json = {
        "status": "success",
        "data": {"interval": 12, "urls": ["192.168.0.1", "1.2.3.4", "ch.pool.ntp.org"]},
    }

    request_json = {"urls": ["1.2.3.4", "ch.pool.ntp.org"]}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/time/ntpconfig",
        "PATCH",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_patch_time_ntp_config(request_json)
    assert isinstance(actual, NtpConfig)
    assert actual.interval == 12


@pytest.mark.asyncio
async def test_async_get_time_suninfo(client_api_auth, mock_aioresponse):
    """Test async_get_time_sun_info."""
    response_json = {
        "status": "success",
        "data": {
            "sunrise": "06:07",
            "sunrise_utc": "04:07",
            "sunset": "20:58",
            "sunset_utc": "18:58",
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/time/suninfo", "GET", response_json
    )

    actual = await client_api_auth.async_get_time_sun_info()
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_time_suninfo_date(client_api_auth, mock_aioresponse):
    """Test async_get_time_sun_info_date."""
    response_json = {
        "status": "success",
        "data": {
            "sunrise": "06:07",
            "sunrise_utc": "04:07",
            "sunset": "20:58",
            "sunset_utc": "18:58",
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/time/suninfo/2024-01-01", "GET", response_json
    )

    actual = await client_api_auth.async_get_time_sun_info_date("2024-01-01")
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_ntp_config_async_refresh(client_api_auth, mock_aioresponse):
    """Test NtpConfig.async_refresh."""
    response_json = {
        "status": "success",
        "data": {"interval": 12, "urls": ["ch.pool.ntp.org"]},
    }

    raw_data = {"interval": 12, "urls": ["192.168.0.1", "ch.pool.ntp.org"]}

    config = NtpConfig(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/time/ntpconfig", "get", response_json
    )

    await config.async_refresh()

    assert config.interval == 12
    assert config.urls == ["ch.pool.ntp.org"]
