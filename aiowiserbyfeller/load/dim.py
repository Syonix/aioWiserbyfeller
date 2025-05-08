"""Support for dimmable light switch devices."""

from __future__ import annotations

from aiowiserbyfeller.const import BUTTON_OFF, BUTTON_ON, EVENT_CLICK

from .load import Load


class Dim(Load):
    """Representation of a dimmable light switch in the Feller Wiser µGateway API."""

    @property
    def state_bri(self) -> int | None:
        """Current brightness of the load."""
        if self.raw_state is None:
            return None

        return self.raw_state["bri"]

    async def async_set_bri(self, bri: int) -> dict:
        """Set new target brightness of the light switch."""
        return await super().async_set_target_state({"bri": bri})

    async def async_switch_on(self) -> dict:
        """Switch on the load.

        Note: This implementation using a button press instead of forcing a target state respects the configured
              turn-on behavior. The Wiser device can be configured to either turn on with 100% brightness or the last
              used value.
        """
        return await super().async_ctrl(BUTTON_ON, EVENT_CLICK)

    async def async_switch_off(self) -> dict:
        """Switch off the load."""
        return await self.async_ctrl(BUTTON_OFF, EVENT_CLICK)
