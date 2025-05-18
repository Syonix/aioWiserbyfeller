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
    def state_temperature(self) -> float | None:
        """Current temperature of the sensor."""
        if self.raw_data is None:
            return None

        return self.raw_data.get("value", None)

    @property
    def unit(self) -> str | None:
        """Unit of the temperature sensor."""
        if self.raw_data is None:
            return None

        return self.raw_data.get("unit", None)

    @property
    def history(self) -> list[TemperatureRecord] | None:
        """List of historical temperature records."""
        if self.raw_data is None or "history" not in self.raw_data:
            return None

        return [
            TemperatureRecord(
                time=datetime.fromisoformat(rec["time"]), value=rec["value"]
            )
            for rec in self.raw_data["history"]
        ]
