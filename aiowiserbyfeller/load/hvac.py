"""Support for hvac (valve) devices."""

from __future__ import annotations

from aiowiserbyfeller.const import STATE_COOLING, STATE_HEATING, STATE_IDLE, STATE_OFF

from .load import Load


class Hvac(Load):
    """Representation of a heating channel (valve) in the Feller Wiser µGateway API."""

    @property
    def state(self) -> str | None:
        """Current state of the heating channel (valve).

        Returns one of STATE_HEATING, STATE_COOLING, STATE_IDLE, STATE_OFF.
        """
        if self.raw_state is None:
            return None

        if self.state_cooling:
            return STATE_COOLING

        if self.state_heating:
            return STATE_HEATING

        if self.boost_temperature == -99:
            return STATE_OFF

        return STATE_IDLE

    @property
    def state_heating(self) -> bool | None:
        """Current heating state of the heating channel (valve)."""
        if self.raw_state is None:
            return None
        return self.flag("output_on") is True and self.flag("cooling") is False

    @property
    def state_cooling(self) -> bool | None:
        """Current cooling state of the heating channel (valve)."""
        if self.raw_state is None:
            return None
        return self.flag("output_on") is True and self.flag("cooling") is True

    @property
    def controller(self) -> str | None:
        """Current name of hvac controller."""
        if self.raw_data is None:
            return None
        return self.raw_data["controller"]

    @property
    def heating_cooling_level(self) -> int | None:
        """Current heating/cooling level of the heating channel (valve).

        Ranges from 0 to 10000
        """
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
    ) -> dict[str, bool]:
        """Current flags of the heating channel (valve).

        Available flags: remote_controlled, sensor_error, valve_error, noise, output_on, cooling
        """
        if self.raw_state is None or "flags" not in self.raw_state:
            return {}

        return {k: bool(v) for k, v in self.raw_state["flags"].items()}

    def flag(self, identifier: str) -> bool | None:
        """Get the value of a specific flag."""
        return self.flags.get(identifier, None)
