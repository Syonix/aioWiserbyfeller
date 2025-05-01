"""Support for hvac (valve) devices."""

from __future__ import annotations

from .load import Load
from typing import Dict
from ..util import validate_str


class Hvac(Load):
    """Representation of a heating channel (valve) in the Feller Wiser µGateway API."""

    @property
    def state(self) -> int | None:
        """Current state of the heating channel (valve)."""
        if self.raw_state is None:
            return None
        return self.flag("state")

    @property
    def controller(self) -> str | None:
        """Current name of hvac controller."""
        if self.raw_state is None:
            return None
        return self.raw_state["controller"]
    
    @property
    def heating_cooling_level(self) -> int | None:
        """Current heating/cooling level of the heating channel (valve).
        Ranges from 0 to 10000"""
        if self.raw_state is None:
            return None
        return self.raw_state["heating_cooling_level"]

    @property
    def target_temperature(self) -> float | None:
        """Current target temperature of the heating channel (valve)."""
        if self.raw_state is None:
            return None
        return self.raw_state["target_temperature"]

    @property
    def boost_temperature(self) -> int | None:
        """Current boost temperature value of the heating channel (valve).
        Possible values: On: 0, Off: -99
        """
        if self.raw_state is None:
            return None
        return self.raw_state["boost_temperature"]

    @property
    def ambient_temperature(self) -> float | None:
        """Current ambient temperature."""
        if self.raw_state is None:
            return None
        return self.raw_state["ambient_temperature"]

    @property
    def unit(self) -> str | None:
        """Current temperature unit of the heating channel (valve)."""
        if self.raw_state is None:
            return None
        return self.raw_state["unit"]

    @property
    def flags(
        self,
    ) -> Dict[str, bool]:
        """Current flags of the heating channel (valve).
        Available flags: remote_controlled, sensor_error, valve_error, noise, output_on, cooling
        """
        if self.raw_state is None or "flags" not in self.raw_state:
            return {}

        return {k: bool(v) for k, v in self.raw_state["flags"].items()}

    def flag(self, identifier: str) -> bool | None:
        """Get the value of a specific flag."""

        validate_str(identifier, ["remote_controlled", "sensor_error", "valve_error", "noise", "output_on", "cooling"])  
        return self.flags[identifier] if identifier in self.flags else None
