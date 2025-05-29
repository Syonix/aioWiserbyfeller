"""Representation of an HVAC group in the Feller Wiser µGateway API."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from aiowiserbyfeller.auth import Auth
from aiowiserbyfeller.const import (
    HTTP_METHOD_DELETE,
    HTTP_METHOD_GET,
    HTTP_METHOD_PATCH,
    HTTP_METHOD_PUT,
)
from aiowiserbyfeller.errors import InvalidState
from aiowiserbyfeller.util import normalize_unit


class HvacChannelState(Enum):
    """Available HVAC channel states."""

    HEATING = "heating"
    COOLING = "cooling"
    IDLE = "idle"
    OFF = "off"
    UNKNOWN = None


class HvacStateProperties:
    """Abstract class with shared properties of HVAC classes with state."""

    @property
    def raw_data(self) -> dict:
        """Raw data dict."""
        return self._raw_data

    @raw_data.setter
    def raw_data(self, raw_data) -> None:
        """Raw data dict setter."""
        if raw_data is None:
            self._raw_data = {}
            self._thermostat_ref = None
            return

        if "state" in raw_data:
            self.raw_state = raw_data["state"]
            del raw_data["state"]

        self._raw_data = raw_data
        self._thermostat_ref = (
            ThermostatReference(
                raw_data["thermostat_ref"]["input_type"],
                raw_data["thermostat_ref"]["input_channel"],
                raw_data["thermostat_ref"]["address"],
            )
            if "thermostat_ref" in raw_data
            else None
        )

    @property
    def state(self) -> HvacChannelState:
        """Current state of the heating channel (valve)."""
        if self.raw_state is None:
            return HvacChannelState.UNKNOWN

        if self.state_cooling:
            return HvacChannelState.COOLING

        if self.state_heating:
            return HvacChannelState.HEATING

        if self.boost_temperature == -99:
            return HvacChannelState.OFF

        return HvacChannelState.IDLE

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
    def thermostat_ref(self) -> ThermostatReference | None:
        """Reference to the linked thermostat."""
        return self._thermostat_ref

    @property
    def heating_cooling_level(self) -> int | None:
        """Current heating/cooling level of the heating channel (valve).

        Ranges from 0 to 10000
        """
        return (
            self.raw_state.get("heating_cooling_level")
            if self.raw_state is not None
            else None
        )

    @property
    def target_temperature(self) -> float | None:
        """Current target temperature of the heating channel (valve)."""
        return (
            self.raw_state.get("target_temperature")
            if self.raw_state is not None
            else None
        )

    @property
    def boost_temperature(self) -> int | None:
        """Current boost temperature value of the heating channel (valve).

        The boost temperature allows the system to over- or undershoot target temperature
        levels without changing them. For example, if the heating source generates more heating or
        cooling power than required, a boost of 1.5 sets the target temperature 1.5°C higher.

        For most setups, this feature is most likely not required.
        """
        return (
            self.raw_state.get("boost_temperature")
            if self.raw_state is not None
            else None
        )

    @property
    def ambient_temperature(self) -> float | None:
        """Current ambient temperature."""
        return (
            self.raw_state.get("ambient_temperature")
            if self.raw_state is not None
            else None
        )

    @property
    def unit(self) -> str | None:
        """Unit of the sensor.

        Note: The API returns the unit character `℃`. This is being normalized
              to `°C` for better compatibility.
        """
        if self.raw_state is None:
            return None

        return normalize_unit(self.raw_state.get("unit"))

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
        return self.flags.get(identifier)


@dataclass
class ThermostatReference:
    """Representation of a thermostat reference object."""

    input_type: int
    input_channel: int
    address: str


class HvacGroup(HvacStateProperties):
    """Class that represents a Feller Wiser HVAC group."""

    def __init__(self, raw_data: dict, auth: Auth, raw_state: dict | None = None):
        """Initialize an HVAC group object."""
        self._thermostat_ref = None
        self._auth = auth
        self.raw_state = raw_state
        self.raw_data = raw_data

    @property
    def id(self) -> int:
        """The HVAC group's ID."""
        return self.raw_data.get("id")

    @property
    def loads(self) -> dict[int]:
        """A list of load ids."""
        return self.raw_data.get("loads")

    @property
    def name(self) -> dict[int]:
        """The HVAC group's name."""
        return self.raw_data.get("name")

    @property
    def max_temperature(self) -> int:
        """The configured maximum target temperature."""
        return self.raw_data.get("max_temperature")

    @property
    def min_temperature(self) -> int:
        """The configured minimum target temperature."""
        return self.raw_data.get("min_temperature")

    @property
    def offset_temperature(self) -> float:
        """The configured offset temperature to correct the measured reading."""
        return self.raw_data.get("offset_temperature")

    @property
    def is_on(self) -> bool | None:
        """Current on state.

        Note: Setting the on state to off is a shortcut to set the boost temperature to -99.
        The heating setup is not truly off: It turns back on, when the ambient temperature
        falls below 3°C to prevent frost damage.
        """
        return self.raw_state.get("on")

    async def async_refresh(self):
        """Fetch data from µGateway."""
        data = await self._auth.request(HTTP_METHOD_GET, f"hvacgroups/{self.id}")
        self.raw_state = data["state"]
        del data["state"]

        self.raw_data = data

    async def async_refresh_state(self):
        """Fetch data from µGateway."""
        data = await self._auth.request(HTTP_METHOD_GET, f"hvacgroups/{self.id}")
        self.raw_state = data["state"]

    async def async_set_target_state(self, target_state: dict):
        """Set target state."""
        data = await self._auth.request(
            HTTP_METHOD_PUT, f"hvacgroups/{self.id}/target_state", json=target_state
        )
        self.raw_state = data["state"]

    async def async_set_target_temperature(self, target_temperature: float):
        """Set target temperature state."""
        return await self.async_set_target_state(
            {"target_temperature": target_temperature}
        )

    async def async_enable(self):
        """Set target state to 'enabled'."""
        return await self.async_set_target_state({"on": True})

    async def async_disable(self):
        """Set target state to 'disabled'."""
        return await self.async_set_target_state({"on": False})

    async def async_replace_loads(self, load_ids: list[int]) -> None:
        """Replace the loads in an existing HVAC-Group."""
        data = await self._auth.request(
            HTTP_METHOD_PUT, f"hvacgroups/{self.id}", json={"loads": load_ids}
        )
        self.raw_data["loads"] = data["loads"]

    async def async_append_loads(self, load_ids: list[int]) -> None:
        """Append more loads to the existing loads list."""
        data = await self._auth.request(
            HTTP_METHOD_PATCH, f"hvacgroups/{self.id}", json={"loads": load_ids}
        )
        self.raw_data["loads"] = data["loads"]

    async def async_get_binding_state(self) -> bool:
        """Ask for HVAC group binding-state."""
        if self.id is None:
            raise InvalidState(
                "Attempting to check binding status for HvacGroup instance without id."
            )

        data = await self._auth.request(HTTP_METHOD_GET, f"hvacgroups/{self.id}/bind")
        return data.get("running", False) is True

    async def async_stop_binding(self) -> bool:
        """Stop HVAC group binding."""
        if self.id is None:
            raise InvalidState(
                "Attempting to stop binding for HvacGroup instance without id."
            )

        data = await self._auth.request(
            HTTP_METHOD_PUT, f"hvacgroups/{self.id}/bind", json={"running": False}
        )
        return data.get("running") is False

    async def async_bind_thermostat(self) -> None:
        """Bind an existing HVAC-Group to a thermostat.

        When this service is called, all the thermostats start flashing. After pressing the
        button of the thermostat, the binding between a HVAC group and a thermostat is created.
        """
        if self.id is None:
            raise InvalidState(
                "Attempting to binding thermostat to HvacGroup instance without id."
            )

        self.raw_data = await self._auth.request(
            HTTP_METHOD_PATCH, f"hvacgroups/{self.id}/bind"
        )

    async def async_delete_thermostat_binding(self):
        """Delete an existing HVAC-Group binding from a thermostat."""
        if self.id is None:
            raise InvalidState(
                "Attempting to delete thermostat binding for HvacGroup instance without id."
            )

        await self._auth.request(HTTP_METHOD_DELETE, f"hvacgroups/{self.id}/bind")
        self._thermostat_ref = None
