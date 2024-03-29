"""Base class for all loads."""
from __future__ import annotations

from ..auth import Auth
from ..util import validate_str


class Load:
    """Base class that represents a load object in the Feller Wiser
    µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth, **kwargs):
        """"""
        self.raw_data = raw_data
        self.raw_state = kwargs.get("raw_state", None)
        self.auth = auth

    @property
    def id(self) -> int:
        """Internal unique id of the load."""
        return self.raw_data["id"]

    @property
    def name(self) -> str:
        """UTF-8 string for the name of a load (e.g. ceiling spots,
        chandeliers, window west, stand lamp) defined by the user"""
        return self.raw_data["name"]

    @property
    def unused(self) -> bool:
        """Flag to indicate that the underlying load is currently not
        used (no load is physically connected to that channel)"""
        return self.raw_data["unused"]

    @property
    def type(self) -> str:
        """A string describing the main-type of the channel the load is
        connected to. Possible values: onoff, dim, motor or dali"""
        return self.raw_data["type"]

    @property
    def sub_type(self) -> str:
        """The channel subtype. Possible values:"""
        return self.raw_data["sub_type"]

    @property
    def device(self) -> str:
        """Reference id to the physical device"""
        return self.raw_data["device"]

    @property
    def channel(self) -> int:
        """Reference id to the physical device"""
        return self.raw_data["channel"]

    @property
    def room(self) -> int:
        """Reference id an id of a room created and deleted by the app."""
        return self.raw_data["room"]

    @property
    def kind(self) -> int | None:
        """Property to store a value that corresponds to the icon
        Possible values for lights: Light:0, Switch:1
        Possible values for covers: Motor:0, Venetian blinds:1,
        Roller shutters:2, Awnings:3"""
        if self.raw_data is None or "kind" not in self.raw_data:
            return None

        return self.raw_data["kind"]

    @property
    def state(self) -> dict | None:
        """Current state of the switch."""
        if self.raw_state is None:
            return None

        return self.raw_state

    async def async_set_target_state(self, data: dict) -> dict:
        """Save new target state to µGateway. Note: A successful response
        assumes target_state as real state.

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
            white: 0..255"""
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
            ["on", "off", "up", "down", "toggle", "stop"],
            error_message="Invalid button value",
        )
        validate_str(
            event,
            [
                "click",  # if the button was pressed shorter than 500ms
                "press",  # if the button was pressed 500ms or longer
                "release",  # must follow after a press event
            ],
            error_message="Invalid button event value",
        )

        json = {"button": button, "event": event}

        return await self.auth.request("put", f"loads/{self.id}/ctrl", json=json)

    async def async_ping(self, time_ms: int, blink_pattern: str, color: str) -> dict:
        """Get the corresponding buttons to control a load lights up."""
        json = {"time_ms": time_ms, "blink_pattern": blink_pattern, "color": color}
        return await self.auth.request("put", f"loads/{self.id}/ping", json=json)
