"""Representation of a Group Ctrl in the Feller Wiser µGateway API."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth


class GroupCtrl:
    """Class that represents a Feller Wiser Group Ctrl."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a GroupCtrl object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int | None:
        """The Group Ctrl's ID."""
        return self.raw_data.get("id")

    @property
    def name(self) -> str | None:
        """The Group Ctrl's name."""
        return self.raw_data.get("name")

    @property
    def type(self) -> str | None:
        """The Group Ctrl's type (`light` or `blinds`)."""
        return self.raw_data.get("type")

    async def async_refresh(self):
        """Fetch data from µGateway."""
        self.raw_data = await self.auth.request("get", f"groupctrls/{self.id}")
