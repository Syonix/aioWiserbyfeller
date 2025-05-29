"""Base class for all loads."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth
from aiowiserbyfeller.const import (
    BUTTON_DOWN,
    BUTTON_OFF,
    BUTTON_ON,
    BUTTON_STOP,
    BUTTON_TOGGLE,
    BUTTON_UP,
    EVENT_CLICK,
    EVENT_PRESS,
    EVENT_RELEASE,
)
from aiowiserbyfeller.util import validate_str


class Load:
    """Base class that represents a load object in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth, **kwargs):
        """Initialize load instance."""
        self.raw_data = raw_data
        self.raw_state = kwargs.get("raw_state")
        self.auth = auth

    @property
    def raw_data(self) -> dict:
        """Raw data dict."""
        return self._raw_data

    @raw_data.setter
    def raw_data(self, raw_data) -> None:
        """Raw data dict setter."""
        self._raw_data = raw_data

    @property
    def id(self) -> int:
        """Internal unique id of the load."""
        return self.raw_data.get("id")

    @property
    def name(self) -> str:
        """UTF-8 string for the name of a load defined by the user.

        (e.g. ceiling spots, chandeliers, window west, stand lamp)
        """
        return self.raw_data.get("name")

    @property
    def unused(self) -> bool:
        """Flag to indicate that the underlying load is currently not used (no load is physically connected to that channel)."""
        return self.raw_data.get("unused")

    @property
    def type(self) -> str:
        """A string describing the main-type of the channel the load is connected to.

        Possible values: onoff, dim, motor or dali
        """
        return self.raw_data.get("type")

    @property
    def sub_type(self) -> str:
        """The channel subtype."""
        return self.raw_data.get("sub_type")

    @property
    def device(self) -> str:
        """Reference id to the physical device."""
        return self.raw_data.get("device")

    @property
    def channel(self) -> int:
        """Channel of the load."""
        return self.raw_data.get("channel")

    @property
    def room(self) -> int:
        """Reference id an id of a room created and deleted by the app."""
        return self.raw_data.get("room")

    @property
    def kind(self) -> int | None:
        """Property to store a value that corresponds to the icon.

        Possible values for lights: Light:0, Switch:1
        Possible values for covers: Motor:0, Venetian blinds:1,
        Roller shutters:2, Awnings:3
        """
        if self.raw_data is None or "kind" not in self.raw_data:
            return None

        return self.raw_data.get("kind")

    @property
    def state(self) -> dict | None:
        """Current state of the switch."""
        if self.raw_state is None:
            return None

        return self.raw_state

    async def async_set_target_state(self, data: dict) -> dict:
        """Save new target state to µGateway.

        Note: A successful response assumes target_state as real state.

        Possible target-state depending on load-type:
            Main-Type  Sub-Type  Attr.
            onoff                bri
            dim                  bri
            motor                level, tilt
            dali                 bri
            dali       tw        bri, ct
            dali       rgb       bri, red, green, blue, white

        Min / max values:
            bri:   0....0000
            level: 0..10000
            tilt:  0..9
            ct:    1000..20000
            red:   0..255
            green: 0..255
            blue:  0..255
            white: 0..255
        """
        data = await self.auth.request(
            "put", f"loads/{self.id}/target_state", json=data
        )
        self.raw_state = data["target_state"]

        return self.raw_state

    async def async_refresh(self):
        """Fetch data from µGateway."""
        self.raw_data = await self.auth.request("get", f"loads/{self.id}")
        await self.async_refresh_state()

    async def async_refresh_state(self):
        """Fetch data from µGateway."""
        data = await self.auth.request("get", f"loads/{self.id}/state")
        self.raw_state = data["state"]

    async def async_ctrl(self, button: str, event: str) -> dict:
        """Invoke a button-event (ctrl) for one load."""
        validate_str(
            button,
            [BUTTON_ON, BUTTON_OFF, BUTTON_UP, BUTTON_DOWN, BUTTON_TOGGLE, BUTTON_STOP],
            error_message="Invalid button value",
        )
        validate_str(
            event,
            [
                EVENT_CLICK,  # if the button was pressed shorter than 500ms
                EVENT_PRESS,  # if the button was pressed 500ms or longer
                EVENT_RELEASE,  # must follow after a press event
            ],
            error_message="Invalid button event value",
        )

        json = {"button": button, "event": event}

        return await self.auth.request("put", f"loads/{self.id}/ctrl", json=json)

    async def async_ping(self, time_ms: int, blink_pattern: str, color: str) -> dict:
        """Get the corresponding buttons to control a load lights up."""
        json = {"time_ms": time_ms, "blink_pattern": blink_pattern, "color": color}
        return await self.auth.request("put", f"loads/{self.id}/ping", json=json)
