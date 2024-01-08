"""Support for timer configuration."""
from __future__ import annotations

from ..auth import Auth


class Timer:
    """Representation of a timer configuration in the Feller Wiser
    µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int | None:
        """[read-only] unique id"""
        return self.raw_data["id"] if "id" in self.raw_data else None

    @property
    def enabled(self) -> bool:
        """Set false if the timer is disabled, else true"""
        return self.raw_data["enabled"]

    @property
    def job(self) -> int:
        """Id of a job to be executed"""
        return self.raw_data["job"]

    @property
    def when(self) -> dict[str]:
        """Time when to run the trigger, with properties every and at:"""
        return self.raw_data["when"]

    async def async_refresh(self):
        """Get current NTP config from µGateway."""
        data = await self.auth.request("get", f"timers/{self.id}")
        self.raw_data = data
