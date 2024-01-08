"""Support for DALI tunable white light switch devices."""
from .load import Load


class DaliTw(Load):
    """Representation of a DALI tunable white light switch in the Feller
    Wiser µGateway API."""

    async def async_control_bri(self, bri: int, ct: int) -> dict:
        """Brightness: 0..10000, Color Temperature: 1000..20000"""
        return await super().async_set_target_state({"bri": bri, "ct": ct})
