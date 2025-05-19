"""Support for scenes."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth


class Scene:
    """Representation of a scene in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a scene object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int | None:
        """The id of the scene."""
        return self.raw_data.get("id")

    @property
    def type(self) -> int:
        """The scene type."""
        return self.raw_data["type"]

    @property
    def kind(self) -> int:
        """The scene kind."""
        return self.raw_data["kind"]

    @property
    def name(self) -> str:
        """The scene name."""
        return self.raw_data["name"]

    @property
    def job(self) -> int:
        """The scene job."""
        return self.raw_data["job"]

    @property
    def scene_buttons(self) -> list[dict]:
        """Scene buttons linked to this scene."""
        return self.raw_data["sceneButtons"]

    async def async_refresh(self):
        """Fetch data from µGateway."""
        data = await self.auth.request("get", f"scenes/{self.id}")
        self.raw_data = data
