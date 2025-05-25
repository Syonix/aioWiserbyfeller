"""Support for rain sensors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .sensor import Sensor


@dataclass
class RainRecord:
    """Representation of a rain sensor history."""

    time: datetime
    value: bool


class Rain(Sensor):
    """Representation of a rain sensor in the Feller Wiser µGateway API."""

    @property
    def value_rain(self) -> bool:
        """Indicates if rain is being detected."""
        return bool(self.value)

    @property
    def history(self) -> list[RainRecord] | None:
        """List of historical rain records."""
        return [
            RainRecord(
                time=datetime.fromisoformat(rec.get("time")),
                value=bool(rec.get("value")),
            )
            for rec in self.raw_data.get("history", [])
        ]
