"""aiowiserbyfeller Api class sensors tests."""

from datetime import datetime

import pytest

from aiowiserbyfeller import Sensor, Temperature

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_sensors(client_api_auth, mock_aioresponse):
    """Test async_get_sensors."""

    response_json = {
        "status": "success",
        "data": [
            {
                "value": 25.3,
                "sub_type": "",
                "type": "temperature",
                "history": [
                    {"time": "2025-05-18T12:42:06+00:00", "value": 25.1},
                    {"time": "2025-05-18T12:52:02+00:00", "value": 25.2},
                    {"time": "2025-05-18T13:11:54+00:00", "value": 25.3},
                ],
                "name": "Room Sensor (0002bc60_0)",
                "device": "0002bc60",
                "id": 31,
                "channel": 0,
                "unit": "℃",
            },
            {
                "value": 21.9,
                "sub_type": "",
                "type": "temperature",
                "name": "Room Sensor (0002bc61_0)",
                "device": "0002bc61",
                "id": 32,
                "channel": 0,
                "unit": "℃",
            },
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/sensors", "get", response_json
    )

    actual = await client_api_auth.async_get_sensors()

    assert len(actual) == 2
    assert isinstance(actual[0], Temperature)
    assert actual[0].id == 31
    assert actual[0].channel == 0
    assert actual[0].state_temperature == 25.3
    assert actual[1].history is None


@pytest.mark.asyncio
async def test_async_get_sensor(client_api_auth, mock_aioresponse):
    """Test async_get_sensor."""

    response_json = {
        "data": {
            "value": 25.3,
            "sub_type": "",
            "type": "temperature",
            "history": [
                {"time": "2025-05-18T12:42:06+00:00", "value": 25.1},
                {"time": "2025-05-18T12:52:02+00:00", "value": 25.2},
                {"time": "2025-05-18T13:11:54+00:00", "value": 25.3},
            ],
            "name": "Room Sensor (0002bc60_0)",
            "device": "0002bc60",
            "id": 31,
            "channel": 0,
            "unit": "℃",
        },
        "status": "success",
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/sensors/31", "get", response_json
    )

    actual = await client_api_auth.async_get_sensor(31)

    assert isinstance(actual, Sensor)
    assert actual.id == 31
    assert actual.name == "Room Sensor (0002bc60_0)"
    assert actual.device == "0002bc60"
    assert actual.history.__len__() == 3
    assert actual.history[0].time == datetime.fromisoformat("2025-05-18T12:42:06+00:00")
