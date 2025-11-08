"""Support for system flags."""

from aiowiserbyfeller.auth import Auth


class SystemFlag:
    """Class that represents system flag in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize.

        Args:
            raw_data: Dict representing the raw API data
            auth: Instance of Auth

        """
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> int:
        """Internal unique id of the system flag."""
        return self.raw_data["id"]

    @property
    def symbol(self) -> str:
        """Symbol of the flag containing only A-Z, a-z, 0-9 and _."""
        return self.raw_data["symbol"]

    @property
    def value(self) -> bool:
        """Current flag value."""
        return self.raw_data["value"]

    @property
    def name(self) -> str:
        """Human-readable name for the flag."""
        return self.raw_data["name"]

    async def async_refresh(self):
        """Fetch data from µGateway."""
        data = await self.auth.request("get", f"system/flags/{self.id}")
        self.raw_data = data

    async def async_set_value(self, value: bool):
        """Enable flag."""
        self.raw_data = await self.auth.request(
            "patch", f"system/flags/{self.id}", json={"value": value}
        )

    async def async_enable(self):
        """Enable flag."""
        await self.async_set_value(True)

    async def async_disable(self):
        """Disable flag."""
        await self.async_set_value(False)

    async def async_toggle(self):
        """Toggle flag."""
        await self.async_set_value(not self.value)
