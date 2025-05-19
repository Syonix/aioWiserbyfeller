"""aiowiserbyfeller Api class sensors tests."""

from datetime import datetime
import json
from pathlib import Path

import pytest

from aiowiserbyfeller import Sensor, Temperature
from aiowiserbyfeller.const import SENSOR_TYPE_TEMPERATURE, UNIT_TEMPERATURE_CELSIUS
from aiowiserbyfeller.errors import NotImplementedSensorType

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


def validate_data(base: str, sensors: list[str]) -> list[dict]:
    """Provide data for test_validate_data_valid, ."""
    result = []

    for sensor in sensors:
        with Path(f"{base}/{sensor}.json").open("r", encoding="utf-8") as f:
            result.append(json.load(f))

    return result


def not_implemented_data() -> list[dict]:
    """Provide data for test_async_get_sensors and test_async_get_sensor."""
    return validate_data(
        "tests/data/sensors/not-implemented",
        [
            "hail_sensor",
            "illuminance_sensor",
            "rain_sensor",
            "wind_sensor",
        ],
    )


def validate_data_valid() -> list[dict]:
    """Provide data for test_async_get_sensors and test_async_get_sensor."""
    return validate_data(
        "tests/data/sensors/valid",
        [
            "temperature_sensor",
            "temperature_sensor_with_history",
        ],
    )


def validate_data_invalid() -> list[dict]:
    """Provide data for test_validate_data_invalid."""
    return validate_data("tests/data/sensors/wrong-unit", ["temperature_sensor"])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("data", "expected_length"),
    [
        (validate_data_valid(), 2),
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
    assert isinstance(actual[0], Temperature)
    assert isinstance(actual[0].id, int)
    assert actual[0].channel == 0
    assert isinstance(actual[0].value_temperature, float)
    assert actual[0].type == SENSOR_TYPE_TEMPERATURE
    assert len(actual[1].history) == 3
    assert actual[1].history[1].time == datetime.fromisoformat(
        "2025-05-18T12:52:02+00:00"
    )
    assert actual[1].unit == UNIT_TEMPERATURE_CELSIUS
    assert actual[1].sub_type is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("data", "expected_error", "expected_unit"),
    [
        (not_implemented_data()[0], NotImplementedSensorType, None),
        (validate_data_valid()[0], None, UNIT_TEMPERATURE_CELSIUS),
        (validate_data_invalid()[0], None, "m/s"),
    ],
)
async def test_async_get_sensor(
    client_api_auth, mock_aioresponse, data, expected_error, expected_unit
):
    """Test async_get_sensor."""

    response_json = {"status": "success", "data": data}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/sensors/{data['id']}", "get", response_json
    )

    if expected_error is not None:
        with pytest.raises(expected_error):
            await client_api_auth.async_get_sensor(data["id"])
        return

    actual = await client_api_auth.async_get_sensor(data["id"])

    assert isinstance(actual, Sensor)
    assert isinstance(actual.id, int)
    assert actual.name == "Room Sensor (0002bc61_0)"
    assert actual.device == "0002bc61"
    assert actual.unit == expected_unit
