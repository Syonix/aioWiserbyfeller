"""Support for system conditions."""

from aiowiserbyfeller.auth import Auth


class SystemCondition:
    """Class that represents system condition in the Feller Wiser µGateway API."""

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
        """Internal unique id of the system condition."""
        return self.raw_data["id"]

    @property
    def expression(self) -> str:
        """Boolean expression for the new condition (example: not absent)."""
        return self.raw_data["expression"]

    @property
    def value(self) -> bool:
        """Current value of the Condition."""
        return self.raw_data["value"]

    @property
    def name(self) -> str:
        """Human-readable name for the condition."""
        return self.raw_data["name"]

    async def async_refresh(self):
        """Fetch data from µGateway."""
        data = await self.auth.request("get", f"system/conditions/{self.id}")
        self.raw_data = data
