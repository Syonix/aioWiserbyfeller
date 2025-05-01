"""Support for motor switch devices."""

from __future__ import annotations

from .load import Load


class Hvac(Load):
    """Representation of a valve in the Feller Wiser µGateway API."""

    @property
    def state(self) -> int | None:
        """Current state of the Valve."""
        if self.raw_state is None:
            return None

        return self.raw_state["flags"]["output_on"]
