"""Support for DALI RGB light switch devices."""

from .dim import Dim


class DaliRgbw(Dim):
    """Representation of a DALI RGBW light switch in the Feller Wiser µGateway API."""

    @property
    def state_rgbw(self) -> dict | None:
        """Current color of the load."""
        if self.raw_state is None:
            return None

        return dict((k, self.raw_state[k]) for k in ("red", "green", "blue", "white"))  # noqa: C402

    # pylint: disable=too-many-arguments

    async def async_set_bri_rgbw(
        self, bri: int, red: int, green: int, blue: int, white: int
    ) -> dict:
        """Select brightness and color.

        Brightness: 0..10000, Red, green, blue, white: 0..255
        """
        data = {"bri": bri, "red": red, "green": green, "blue": blue, "white": white}
        return await super().async_set_target_state(data)
