"""Support for motor switch devices."""

from __future__ import annotations

from aiowiserbyfeller.const import BUTTON_STOP, EVENT_CLICK

from .load import Load


class Motor(Load):
    """Representation of a motor (cover, venetian blinds, roller shutters, awning) switch in the Feller Wiser µGateway API."""

    @property
    def state(self) -> dict | None:
        """Current state of the motor."""
        if self.raw_state is None:
            return None

        return self.raw_state

    async def async_set_level(self, level: int) -> dict:
        """Set the target level of the cover (0..10000)."""
        return await super().async_set_target_state({"level": level})

    async def async_set_tilt(self, tilt: int) -> dict:
        """Set the target tilt of the cover (0..9)."""
        return await super().async_set_target_state({"tilt": tilt})

    async def async_stop(self):
        """Stop the cover movement."""
        await super().async_ctrl(BUTTON_STOP, EVENT_CLICK)
        await self.async_refresh_state()
