"""Support for hvac (valve) devices."""

from __future__ import annotations

from aiowiserbyfeller.hvac import HvacStateProperties

from .load import Load


class Hvac(HvacStateProperties, Load):
    """Representation of a heating channel (valve) in the Feller Wiser µGateway API."""

    @property
    def controller(self) -> str | None:
        """Current name of hvac controller."""
        return self.raw_data.get("controller") if self.raw_data is not None else None
