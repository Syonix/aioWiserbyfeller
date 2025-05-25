"""aiowiserbyfeller Api class sensors tests."""

from datetime import datetime
import json
from pathlib import Path

import pytest

from aiowiserbyfeller import Brightness, Hail, Rain, Sensor, Temperature, Wind
from aiowiserbyfeller.const import SENSOR_TYPE_TEMPERATURE, UNIT_TEMPERATURE_CELSIUS

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


def validate_data(base: str, sensors: list[str]) -> list[dict]:
    """Provide data for test_validate_data_valid, ."""
    result = []

    for sensor in sensors:
        with Path(f"{base}/{sensor}.json").open("r", encoding="utf-8") as f:
            result.append(json.load(f))

    return result


def validate_data_valid() -> list[dict]:
    """Provide data for test_async_get_sensors and test_async_get_sensor."""
    return validate_data(
        "tests/data/sensors/valid",
        [
            "brightness_sensor",
            "brightness_sensor_with_history",
            "hail_sensor",
            "hail_sensor_with_history",
            "rain_sensor",
            "rain_sensor_with_history",
            "temperature_sensor",
            "temperature_sensor_with_history",
            "wind_sensor",
            "wind_sensor_with_history",
        ],
    )


def validate_data_invalid() -> list[dict]:
    """Provide data for test_validate_data_invalid."""
    return validate_data("tests/data/sensors/wrong-unit", ["temperature_sensor"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("data", "expected_length"),
    [
        (validate_data_valid(), 10),
    ],
)
async def test_async_get_sensors(
    client_api_auth, mock_aioresponse, data, expected_length
):
    """Test async_get_sensors."""

    response_json = {"status": "success", "data": data}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/sensors", "get", response_json
    )

    actual = await client_api_auth.async_get_sensors()

    assert len(actual) == expected_length

    # Brightness
    assert isinstance(actual[0], Brightness)
    assert actual[0].value_brightness == 10

    # Brightness with history
    assert len(actual[1].history) == 3
    assert actual[1].history[1].time == datetime.fromisoformat(
        "2025-05-18T12:52:02+00:00"
    )
    assert actual[1].history[1].value == 5

    # Hail
    assert isinstance(actual[2], Hail)
    assert actual[2].value_hail is False

    # Hail with history
    assert len(actual[3].history) == 3
    assert actual[3].history[1].time == datetime.fromisoformat(
        "2025-05-18T12:52:02+00:00"
    )
    assert actual[3].history[1].value is True

    # Rain
    assert isinstance(actual[4], Rain)
    assert actual[4].value_rain is False

    # Rain with history
    assert len(actual[5].history) == 3
    assert actual[5].history[1].time == datetime.fromisoformat(
        "2025-05-18T12:52:02+00:00"
    )
    assert actual[5].history[1].value is True

    # Temperature
    assert isinstance(actual[6], Temperature)
    assert isinstance(actual[6].id, int)
    assert actual[6].channel == 0
    assert isinstance(actual[6].value_temperature, float)
    assert actual[6].type == SENSOR_TYPE_TEMPERATURE

    # Temperature with history
    assert len(actual[7].history) == 3
    assert actual[7].history[1].time == datetime.fromisoformat(
        "2025-05-18T12:52:02+00:00"
    )
    assert actual[7].unit == UNIT_TEMPERATURE_CELSIUS
    assert actual[7].sub_type is None

    # Wind
    assert isinstance(actual[8], Wind)
    assert actual[8].value_wind_speed == 10

    # Wind with history
    assert len(actual[9].history) == 3
    assert actual[9].history[1].time == datetime.fromisoformat(
        "2025-05-18T12:52:02+00:00"
    )
    assert actual[9].history[1].value == 5


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("data", "expected_unit"),
    [
        (validate_data_valid()[6], UNIT_TEMPERATURE_CELSIUS),
        (validate_data_invalid()[0], "m/s"),
    ],
)
async def test_async_get_sensor(client_api_auth, mock_aioresponse, data, expected_unit):
    """Test async_get_sensor."""

    response_json = {"status": "success", "data": data}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/sensors/{data['id']}", "get", response_json
    )

    actual = await client_api_auth.async_get_sensor(data["id"])

    assert isinstance(actual, Sensor)
    assert isinstance(actual.id, int)
    assert actual.name == "Room Sensor (0002bc61_0)"
    assert actual.device == "0002bc61"
    assert actual.unit == expected_unit
