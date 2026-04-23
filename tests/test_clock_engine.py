import unittest

from application.clock_engine import ClockEngine
from domain.value_objects.clock_time import ClockTime


class FakeTimeService:
    def __init__(self, initial_time: ClockTime) -> None:
        self._initial_time = initial_time

    def get_system_time(self) -> ClockTime:
        return self._initial_time


class TestClockEngine(unittest.TestCase):
    def test_seconds_rollover_and_minute_increment(self) -> None:
        engine = ClockEngine(FakeTimeService(ClockTime(0, 0, 58)))

        after_first_tick = engine.tick()
        self.assertEqual(after_first_tick, ClockTime(0, 0, 59))

        after_second_tick = engine.tick()
        self.assertEqual(after_second_tick, ClockTime(0, 1, 0))

    def test_minutes_rollover_and_hour_increment(self) -> None:
        engine = ClockEngine(FakeTimeService(ClockTime(10, 59, 59)))

        result = engine.tick()
        self.assertEqual(result, ClockTime(11, 0, 0))

    def test_full_day_rollover(self) -> None:
        engine = ClockEngine(FakeTimeService(ClockTime(23, 59, 59)))

        result = engine.tick()
        self.assertEqual(result, ClockTime(0, 0, 0))

    def test_full_backward_rollover(self) -> None:
        engine = ClockEngine(FakeTimeService(ClockTime(0, 0, 0)))

        result = engine.move_backward_one_second()
        self.assertEqual(result, ClockTime(23, 59, 59))


if __name__ == "__main__":
    unittest.main()
