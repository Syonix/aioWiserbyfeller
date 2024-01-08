"""Support for DALI RGB light switch devices."""
from .load import Load


class DaliRgbw(Load):
    """Representation of a DALI RGBW light switch in the Feller Wiser
    µGateway API."""

    # pylint: disable=too-many-arguments

    async def async_control_bri(
        self, bri: int, red: int, green: int, blue: int, white: int
    ) -> dict:
        """Brightness: 0..10000, Red, green, blue, white: 0..255"""
        data = {"bri": bri, "red": red, "green": green, "blue": blue, "white": white}
        return await super().async_set_target_state(data)
