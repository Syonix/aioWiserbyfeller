"""Support for humidity sensors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .sensor import Sensor


@dataclass
class HumidityRecord:
    """Representation of a humidity sensor history."""

    time: datetime
    value: float


class Humidity(Sensor):
    """Representation of a humidity sensor in the Feller Wiser µGateway API."""

    @property
    def value_humidity(self) -> float:
        """Current relative humidity."""
        return self.value

    @property
    def history(self) -> list[HumidityRecord] | None:
        """List of historical humidity records."""
        return [
            HumidityRecord(
                time=datetime.fromisoformat(rec.get("time")), value=rec.get("value")
            )
            for rec in self.raw_data.get("history", [])
        ]
