"""Representation of a device in the Feller Wiser µGateway API."""

from __future__ import annotations

from aiowiserbyfeller.auth import Auth
from aiowiserbyfeller.errors import UnexpectedGatewayResponse
from aiowiserbyfeller.map import DEVICE_ALLOWED_EMPTY_FIELDS, DEVICE_CHECK_FIELDS
from aiowiserbyfeller.util import get_device_name_by_fwid, get_device_name_by_hwid_a


class Device:
    """Class that represents a physical Feller Wiser device."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize a device object."""
        self.raw_data = raw_data
        self.auth = auth
        self._a_name = get_device_name_by_hwid_a(raw_data.get("a", {}).get("hw_id"))
        self._c_name = get_device_name_by_fwid(raw_data.get("c", {}).get("fw_id"))

    @property
    def id(self) -> str | None:
        """Internal device id.

        Note: This is equal to the A block (actuator module) K+ address. K+ addresses are
              globally unique and only ever assigned to one device (similar to a MAC
              address). If you want to identify a unique device combination, use the
              combined_serial_number property, as only the A block has a K+ address.
              Therefore, if the C block is exchanged, the combined serial number changes,
              but the A block address and thus device id remains the same.
        """
        return self.raw_data.get("id")

    @property
    def last_seen(self) -> int | None:
        """Seconds since the device was last seen on the kPlus network."""
        return self.raw_data.get("last_seen")

    @property
    def a(self) -> dict:
        """Information about the actuator module (Funktionseinsatz)."""
        return self.raw_data.get("a", {})

    @property
    def a_name(self) -> str:
        """Name of the actuator module (Funktionseinsatz)."""
        return self._a_name

    @property
    def a_device_family(self) -> int | None:
        """Return the device family identifier.

        The A block hardware ID (self.a["hw_id"]) is a bit field of 2 bytes.
        Those bytes contain four values: type, features, channels and a hardware revision.
        See aiowiserbyfeller.util.parse_wiser_device_hwid_a for technical details.

        The device family is very similar to the hardware ID, but omits the channel number
        and revision information.
        This allows for identifying multiple devices of the same type (e.g. on/off switch 1K, 2K)
        without having to list each device explicitly.

        # +----+----+----+----+----+----+----+----+----+
        # |  0 |   channel_type    |  channel_features |
        # +----+----+----+----+----+----+----+----+----+
        """
        hw_id = self.a.get("hw_id", "")

        if hw_id == "":
            return None

        hw_id = int(hw_id, 16)
        device_type = (hw_id >> 8) & 0x0F
        device_features = (hw_id >> 4) & 0x0F

        return (device_type << 4) | device_features

    @property
    def c(self) -> dict:
        """Information about the control module (Bedienaufsatz)."""
        return self.raw_data.get("c", {})

    @property
    def c_name(self) -> str:
        """Name of the control module (Bedienaufsatz)."""
        return self._c_name

    @property
    def inputs(self) -> list:
        """List of inputs (e.g. buttons)."""
        return self.raw_data.get("inputs", [])

    @property
    def outputs(self) -> list:
        """List of outputs (e.g. lights or covers)."""
        return self.raw_data.get("outputs", [])

    @property
    def combined_serial_number(self) -> str | None:
        """The combination of the A and C block serial numbers.

        As wiser devices always consist of two components, offer a combined
        serial number. This should be used as serial number, as changing out
        one of the component might change the feature set of the whole device.

        Note that non-modular devices (e.g. valve controller) do send an empty
        serial_nr for the C block.
        """
        return (
            f"{self.c.get('serial_nr')} / {self.a.get('serial_nr')}"
            if self.c.get("serial_nr", "") != ""
            else self.a.get("serial_nr")
        )

    def validate_data(self):
        """Validate if the API has sent all device identifying data fields.

        More information about why this method exists: https://github.com/Feller-AG/wiser-api/issues/43
        """
        for key in DEVICE_CHECK_FIELDS:
            for prop in DEVICE_CHECK_FIELDS[key]:
                if getattr(self, key)[prop] != "":
                    continue

                if prop in DEVICE_ALLOWED_EMPTY_FIELDS.get(
                    self.a_device_family, {}
                ).get(key, []):
                    continue

                # Re-enable the following lines when needed.
                # hw_id = self.a.get("hw_id", "")
                # if prop in DEVICE_ALLOWED_EMPTY_FIELDS.get(hw_id, {}).get(key, []):
                #    continue

                raise UnexpectedGatewayResponse(
                    f"Invalid API response: Device {self.id} has an empty field {key}.{prop}!"
                )

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
