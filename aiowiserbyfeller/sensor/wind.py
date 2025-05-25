"""Support for wind sensors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .sensor import Sensor


@dataclass
class WindRecord:
    """Representation of a wind sensor history."""

    time: datetime
    value: int


class Wind(Sensor):
    """Representation of a wind sensor in the Feller Wiser µGateway API."""

    @property
    def value_wind_speed(self) -> int:
        """Current wind speed."""
        return self.value

    @property
    def history(self) -> list[WindRecord] | None:
        """List of historical wind speed records."""
        return [
            WindRecord(
                time=datetime.fromisoformat(rec.get("time")), value=rec.get("value")
            )
            for rec in self.raw_data.get("history", [])
        ]
