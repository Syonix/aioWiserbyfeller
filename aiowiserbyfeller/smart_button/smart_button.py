"""Support for smart button configuration."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth


class SmartButton:
    """Representation of a smart button configuration in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a smart button object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int | None:
        """[read-only] unique id."""
        return self.raw_data["id"]

    @property
    def job(self) -> int:
        """ID of a job."""
        return self.raw_data["job"]

    @property
    def device(self) -> str:
        """Device of the smart button."""
        return self.raw_data["device"]

    @property
    def device_addr(self) -> int:
        """Device address of the smart button."""
        return self.raw_data["device_addr"]

    @property
    def input_channel(self) -> int:
        """Input channel of the smart button."""
        return self.raw_data["input_channel"]

    @property
    def input_type(self) -> int:
        """Input type of the smart button.

        Possible values are not documented.
        """
        return self.raw_data["input_type"]

    async def async_refresh(self):
        """Fetch data from µGateway."""
        self.raw_data = await self.auth.request("get", f"smartbuttons/{self.id}")
