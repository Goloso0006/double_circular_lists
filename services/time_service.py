from __future__ import annotations

from datetime import datetime

from domain.value_objects.clock_time import ClockTime


class TimeService:
    """Servicio para obtener la hora real del sistema."""

    def get_system_time(self) -> ClockTime:
        now = datetime.now()
        return ClockTime(hour=now.hour, minute=now.minute, second=now.second)
