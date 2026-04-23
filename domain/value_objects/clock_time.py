from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClockTime:
    """Value object inmutable para transportar hora actual del reloj."""

    hour: int
    minute: int
    second: int

    def to_12_hour_format(self) -> str:
        period = "AM" if self.hour < 12 else "PM"
        if self.hour == 0:
            hour_12 = 12
        elif self.hour > 12:
            hour_12 = self.hour - 12
        else:
            hour_12 = self.hour
        return f"{hour_12:02d}:{self.minute:02d}:{self.second:02d} {period}"

    def to_24_hour_format(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
