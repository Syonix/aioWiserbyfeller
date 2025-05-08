"""Support for DALI tunable white light switch devices."""

from .dim import Dim


class DaliTw(Dim):
    """Representation of a DALI tunable white light switch in the Feller Wiser µGateway API."""

    @property
    def state_ct(self) -> int | None:
        """Current color temperature of the load."""
        if self.raw_state is None:
            return None

        return self.raw_state["ct"]

    async def async_set_bri_ct(self, bri: int, ct: int) -> dict:
        """Set brightness and color temperature.

        Brightness: 0..10000, Color Temperature: 1000..20000
        """
        return await super().async_set_target_state({"bri": bri, "ct": ct})
