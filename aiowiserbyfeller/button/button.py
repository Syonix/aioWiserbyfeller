"""Support for button configuration."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth
from aiowiserbyfeller.enum import BlinkPattern


class Button:
    """Representation of a button in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a button object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int | None:
        """[read-only] unique id, or null if the button is not registered."""
        return self.raw_data.get("id")

    @property
    def device(self) -> str:
        """[read-only] reference id to the physical device."""
        return self.raw_data.get("device")

    @property
    def channel(self) -> int:
        """[read-only] input channel of the physical device."""
        return self.raw_data.get("channel")

    @property
    def type(self) -> str:
        """[read-only] type of the input (e.g. `button`)."""
        return self.raw_data.get("type")

    @property
    def sub_type(self) -> str:
        """[read-only] sub-type of the button (e.g. `up down`)."""
        return self.raw_data.get("sub_type", "")

    async def async_refresh(self):
        """Fetch data from µGateway."""
        self.raw_data = await self.auth.request("get", f"buttons/{self.id}")

    async def async_ping(
        self, time_ms: int, blink_pattern: BlinkPattern, color: str
    ) -> dict:
        """Light up the button LED with custom values."""
        json = {
            "time_ms": time_ms,
            "blink_pattern": blink_pattern.value,
            "color": color,
        }
        return await self.auth.request("put", f"buttons/{self.id}/ping", json=json)

    async def async_set_led(
        self,
        led_index: int,
        on: bool,
        pattern: BlinkPattern = BlinkPattern.PERMANENT,
        color: str = "#000000",
    ) -> dict:
        """Set the color, pattern, and enable state of an individual LED on this button."""
        return await self.auth.request(
            "put",
            f"buttons/{self.id}/leds/{led_index}",
            json={
                "on": on,
                "pattern": pattern.value,
                "color": color,
            },
        )
