"""Support for brightness sensors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .sensor import Sensor


@dataclass
class BrightnessRecord:
    """Representation of a brightness sensor history."""

    time: datetime
    value: int


class Brightness(Sensor):
    """Representation of a brightness sensor in the Feller Wiser µGateway API."""

    @property
    def value_brightness(self) -> int:
        """Current brightness."""
        return self.value

    @property
    def history(self) -> list[BrightnessRecord] | None:
        """List of historical brightness records."""
        return [
            BrightnessRecord(
                time=datetime.fromisoformat(rec.get("time")), value=rec.get("value")
            )
            for rec in self.raw_data.get("history", [])
        ]
