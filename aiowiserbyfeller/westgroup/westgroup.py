"""Support for WEST-Groups (Weather Shield Technology)."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth


class WestGroup:
    """Representation of a WEST-Group in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a WEST-Group object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int | None:
        """The id of the WEST-Group."""
        return self.raw_data.get("id")

    @property
    def loads(self) -> list[int]:
        """List of load ids."""
        return self.raw_data.get("loads", [])

    @property
    def wind(self) -> dict:
        """Wind weather protection configuration."""
        return self.raw_data.get("wind", {})

    @property
    def temperature(self) -> dict:
        """Temperature weather protection configuration."""
        return self.raw_data.get("temperature", {})

    @property
    def rain(self) -> dict:
        """Rain weather protection configuration."""
        return self.raw_data.get("rain", {})

    @property
    def hail(self) -> dict:
        """Hail weather protection configuration."""
        return self.raw_data.get("hail", {})

    async def async_refresh(self):
        """Fetch data from µGateway."""
        self.raw_data = await self.auth.request("get", f"westgroups/{self.id}")
