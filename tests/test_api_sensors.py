"""aiowiserbyfeller Api class sensors tests."""

from datetime import datetime
import json
from pathlib import Path

import pytest

from aiowiserbyfeller import Sensor, Temperature
from aiowiserbyfeller.const import SENSOR_TYPE_TEMPERATURE, UNIT_TEMPERATURE_CELSIUS

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


def validate_data(base: str) -> list[dict]:
    """Provide data for test_validate_data_valid."""
    result = []

    for sensor in [
        "temperature_sensor_with_history",
        "temperature_sensor",
    ]:
        with Path(f"{base}/{sensor}.json").open("r", encoding="utf-8") as f:
            result.append(json.load(f))

    return result


def validate_data_valid() -> list[dict]:
    """Provide data for test_validate_data_valid."""
    return validate_data("tests/data/sensors/valid")


@pytest.mark.asyncio
async def test_async_get_sensors(client_api_auth, mock_aioresponse):
    """Test async_get_sensors."""

    response_json = {"status": "success", "data": validate_data_valid()}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/sensors", "get", response_json
    )

    actual = await client_api_auth.async_get_sensors()

    assert len(actual) == 2
    assert isinstance(actual[0], Temperature)
    assert actual[0].id == 31
    assert actual[0].channel == 0
    assert actual[0].value_temperature == 25.3
    assert actual[0].type == SENSOR_TYPE_TEMPERATURE
    assert actual[1].history == []
    assert actual[1].unit == UNIT_TEMPERATURE_CELSIUS
    assert actual[1].sub_type is None


@pytest.mark.asyncio
async def test_async_get_sensor(client_api_auth, mock_aioresponse):
    """Test async_get_sensor."""
    data = validate_data_valid()[0]

    response_json = {"status": "success", "data": data}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/sensors/31", "get", response_json
    )

    actual = await client_api_auth.async_get_sensor(31)

    assert isinstance(actual, Sensor)
    assert actual.id == 31
    assert actual.name == "Room Sensor (0002bc60_0)"
    assert actual.device == "0002bc60"
    assert len(actual.history) == 3
    assert actual.history[0].time == datetime.fromisoformat("2025-05-18T12:42:06+00:00")
