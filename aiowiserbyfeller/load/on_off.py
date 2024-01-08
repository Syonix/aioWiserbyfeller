"""Support for On/Off switch devices."""
from __future__ import annotations

from .load import Load


class OnOff(Load):
    """Representation of an on/off switch in the Feller Wiser µGateway API."""

    @property
    def state(self) -> bool | None:
        """Current state of the switch."""
        if self.raw_state is None:
            return None

        return self.raw_state["bri"] > 0

    async def async_control_onoff(self, state: bool) -> dict:
        """Set new target state of the light switch."""
        bri = 10000 if state else 0
        return await super().async_set_target_state({"bri": bri})

    async def async_control_on(self) -> dict:
        """Set new target state of the switch to on."""
        return await self.async_control_onoff(True)

    async def async_control_off(self) -> dict:
        """Set new target state of the switch to of."""
        return await self.async_control_onoff(False)
