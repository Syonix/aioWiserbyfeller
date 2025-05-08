"""Support for On/Off switch devices."""

from __future__ import annotations

from aiowiserbyfeller.const import BUTTON_OFF, BUTTON_ON, EVENT_CLICK

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
        if state:
            return await self.async_control_on()
        else:
            return await self.async_control_off()

    async def async_control_on(self) -> dict:
        """Set new target state of the switch to on."""
        return await self.async_ctrl(BUTTON_ON, EVENT_CLICK)

    async def async_control_off(self) -> dict:
        """Set new target state of the switch to off."""
        return await self.async_ctrl(BUTTON_OFF, EVENT_CLICK)
