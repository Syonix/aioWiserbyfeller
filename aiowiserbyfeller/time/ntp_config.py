"""Support for ntp time configuration."""

from aiowiserbyfeller.auth import Auth


class NtpConfig:
    """Representation of an NTP time configuration in the Feller Wiser µGateway API."""

    def __init__(self, raw_data: dict, auth: Auth):
        """Initialize n NTP config object."""
        self.raw_data = raw_data
        self.auth = auth

    @property
    def interval(self) -> int:
        """Interval in hours to try NTP or 0 to disable NTP."""
        return self.raw_data["interval"]

    @property
    def urls(self) -> list:
        """List of URL or IP strings that defines which NTP servers to try in what order (without duplicates). May be empty."""
        return self.raw_data["urls"]

    async def async_refresh(self):
        """Get current NTP config from µGateway."""
        data = await self.auth.request("get", "time/ntpconfig")
        self.raw_data = data
