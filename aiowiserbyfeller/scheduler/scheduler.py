"""Support for schedulers."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth


class Scheduler:
    """Representation of a scheduler in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a scheduler object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int | None:
        """The id of the scheduler."""
        return self.raw_data.get("id")

    @property
    def name(self) -> str | None:
        """Name of the scheduler."""
        return self.raw_data.get("name")

    @property
    def icon(self) -> str | None:
        """Icon filename for the scheduler."""
        return self.raw_data.get("icon")

    async def async_refresh(self):
        """Fetch data from µGateway."""
        self.raw_data = await self.auth.request("get", f"schedulers/{self.id}")
