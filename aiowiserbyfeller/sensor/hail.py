"""Support for hail sensors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .sensor import Sensor


@dataclass
class HailRecord:
    """Representation of a hail sensor history."""

    time: datetime
    value: bool


class Hail(Sensor):
    """Representation of a hail sensor in the Feller Wiser µGateway API."""

    @property
    def value_hail(self) -> bool:
        """Indicates if hail is being detected."""
        return bool(self.value)

    @property
    def history(self) -> list[HailRecord] | None:
        """List of historical hail records."""
        return [
            HailRecord(
                time=datetime.fromisoformat(rec.get("time")),
                value=bool(rec.get("value")),
            )
            for rec in self.raw_data.get("history", [])
        ]
