"""Support for window sensors."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .sensor import Sensor


@dataclass
class WindowRecord:
    """Representation of a window sensor history."""

    time: datetime
    value: bool


class Window(Sensor):
    """Representation of a window sensor in the Feller Wiser µGateway API."""

    @property
    def value_window(self) -> bool:
        """Indicates if the window is open."""
        return bool(self.value)

    @property
    def history(self) -> list[WindowRecord] | None:
        """List of historical window state records."""
        return [
            WindowRecord(
                time=datetime.fromisoformat(rec.get("time")),
                value=bool(rec.get("value")),
            )
            for rec in self.raw_data.get("history", [])
        ]
