"""Representation of a device in the Feller Wiser µGateway API."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth


class Device:
    """Class that represents a physical Feller Wiser device."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a device object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> str:
        """Internal device id.

        Note: This is equal to the A block (actuator module) K+ address. K+ addresses are
              globally unique and only ever assigned to one device (similar to a MAC
              address). If you want to identify a unique device combination, use the
              combined_serial_number property, as only the A block has a K+ address.
              Therefore, if the C block is exchanged, the combined serial number changes,
              but the A block address and thus device id remains the same.
        """
        return self.raw_data["id"]

    @property
    def last_seen(self) -> int:
        """Seconds since the device was last seen on the kPlus network."""
        return self.raw_data["last_seen"]

    @property
    def a(self) -> dict:
        """Information about the actuator module (Funktionseinsatz)."""
        return self.raw_data["a"]

    @property
    def c(self) -> dict:
        """Information about the control module (Bedienaufsatz)."""
        return self.raw_data["c"]

    @property
    def inputs(self) -> list:
        """List of inputs (e.g. buttons)."""
        return self.raw_data["inputs"]

    @property
    def outputs(self) -> list:
        """List of outputs (e.g. lights or covers)."""
        return self.raw_data["outputs"]

    @property
    def combined_serial_number(self) -> str:
        """The combination of the A and C block serial numbers.

        As wiser devices always consist of two components, offer a combined
        serial number. This should be used as serial number, as changing out
        one of the component might change the feature set of the whole device.
        """
        return f"{self.c['serial_nr']} / {self.a['serial_nr']}"

    async def async_ping(self) -> bool:
        """Light up the yellow LEDs of all buttons for a short time."""
        resp = await self.auth.request("get", f"devices/{self.id}/ping")

        return resp["ping"] == "pong"

    async def async_status(
        self, channel: int, color: str, background_bri: int, foreground_bri: int | None
    ) -> None:
        """Set status light of load."""

        if foreground_bri is None:
            foreground_bri = background_bri

        data = {
            "color": color,
            "background_bri": background_bri,
            "foreground_bri": foreground_bri,
        }

        config = await self.auth.request("get", f"devices/{self.id}/config")

        await self.auth.request(
            "put", f"devices/config/{config['id']}/inputs/{channel}", json=data
        )

        await self.auth.request("put", f"devices/config/{config['id']}")
