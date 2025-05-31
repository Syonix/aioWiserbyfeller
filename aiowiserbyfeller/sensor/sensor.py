"""Support for sensors."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth
from aiowiserbyfeller.util import normalize_unit


class Sensor:
    """Representation of a sensor in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a sensor object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int | None:
        """The id of the sensor."""
        return self.raw_data.get("id")

    @property
    def type(self) -> str | None:
        """The type of the sensor."""
        return self.raw_data.get("type")

    @property
    def sub_type(self) -> str | None:
        """The subtype of the sensor."""
        return self.raw_data.get("subtype")

    @property
    def name(self) -> str | None:
        """UTF-8 string for the name of a load defined by the user.

        (e.g. ceiling spots, chandeliers, window west, floor lamp)
        """
        return self.raw_data["name"]

    @property
    def value(self) -> float | bool | None:
        """Current state of the sensor."""
        return self.raw_data.get("value")

    @property
    def unit(self) -> str | None:
        """Unit of the sensor.

        Note: The API returns the unit character `℃`. This is being normalized
              to `°C` for better compatibility.
        """
        return normalize_unit(self.raw_data.get("unit"))

    @property
    def device(self) -> str:
        """Reference id to the physical device."""
        return self.raw_data["device"]

    @property
    def channel(self) -> int:
        """Channel of the load."""
        return self.raw_data["channel"]
