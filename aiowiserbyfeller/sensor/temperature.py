"""Support for temperature sensors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .sensor import Sensor


@dataclass
class TemperatureRecord:
    """Representation of a temperature sensor history."""

    time: datetime
    value: float


class Temperature(Sensor):
    """Representation of a temperature sensor in the Feller Wiser µGateway API."""

    @property
    def value_temperature(self) -> float:
        """Current temperature."""
        return self.value

    @property
    def history(self) -> list[TemperatureRecord] | None:
        """List of historical temperature records."""
        return [
            TemperatureRecord(
                time=datetime.fromisoformat(rec.get("time")), value=rec.get("value")
            )
            for rec in self.raw_data.get("history", [])
        ]
