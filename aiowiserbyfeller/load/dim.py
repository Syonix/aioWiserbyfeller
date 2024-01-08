"""Support for dimmable light switch devices."""
from __future__ import annotations

from .load import Load


class Dim(Load):
    """Representation of a dimmable light switch in the Feller Wiser
    µGateway API."""

    @property
    def state(self) -> int | None:
        """Current state of the switch."""
        if self.raw_state is None:
            return None

        return self.raw_state["bri"]

    async def async_control_bri(self, bri: int) -> dict:
        """Set new target brightness of the light switch."""
        return await super().async_set_target_state({"bri": bri})
