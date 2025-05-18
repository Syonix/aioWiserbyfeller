"""Support for sensors."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth


class Sensor:
    """Representation of a sensor in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a job object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int:
        """The id of the sensor."""
        return self.raw_data.get("id", None)

    @property
    def type(self) -> str:
        """The type of the sensor."""
        return self.raw_data.get("type")

    @property
    def sub_type(self) -> str:
        """The subtype of the sensor."""
        return self.raw_data.get("subtype")

    @property
    def name(self) -> str:
        """UTF-8 string for the name of a load defined by the user.

        (e.g. ceiling spots, chandeliers, window west, stand lamp)
        """
        return self.raw_data["name"]

    @property
    def value(self) -> float | None:
        """Current state of the sensor."""
        return self.raw_data.get("value")

    @property
    def unit(self) -> str:
        """Unit of the sensor."""
        return self.raw_data.get("unit")

    @property
    def device(self) -> str:
        """Reference id to the physical device."""
        return self.raw_data["device"]

    @property
    def channel(self) -> int:
        """Channel of the load."""
        return self.raw_data["channel"]
