"""Support for motor switch devices."""
from __future__ import annotations

from .load import Load


class Motor(Load):
    """Representation of a motor (cover, venetian blinds, roller
    shutters, awning) switch in the Feller Wiser µGateway API."""

    @property
    def state(self) -> dict | None:
        """Current state of the motor."""
        if self.raw_state is None:
            return None

        return self.raw_state

    async def async_control_level(self, level: int, tilt: int) -> dict:
        """Level: 0..10000, Tilt: 0..9"""
        return await super().async_set_target_state({"level": level, "tilt": tilt})
