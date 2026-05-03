"""Support for CO2 sensors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .sensor import Sensor


@dataclass
class Co2Record:
    """Representation of a CO2 sensor history."""

    time: datetime
    value: float


class Co2(Sensor):
    """Representation of a CO2 sensor in the Feller Wiser µGateway API."""

    @property
    def value_co2(self) -> float:
        """Current CO2 concentration in ppm."""
        return self.value

    @property
    def history(self) -> list[Co2Record] | None:
        """List of historical CO2 records."""
        return [
            Co2Record(
                time=datetime.fromisoformat(rec.get("time")), value=rec.get("value")
            )
            for rec in self.raw_data.get("history", [])
        ]
