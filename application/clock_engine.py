from __future__ import annotations

from domain.entities.clock_hand import ClockHand
from domain.structures.circular_doubly_linked_list import CircularDoublyLinkedList
from domain.value_objects.clock_time import ClockTime
from services.time_service import TimeService


class ClockEngine:
    """Orquesta la simulacion del reloj analogico."""

    def __init__(self, time_service: TimeService) -> None:
        self.__time_service = time_service

        self.__seconds_values = self.__build_circular_values(0, 59)
        self.__minutes_values = self.__build_circular_values(0, 59)
        self.__hours_values = self.__build_circular_values(0, 23)

        system_time = self.__time_service.get_system_time()
        self.__hour_hand = ClockHand(self.__hours_values, system_time.hour)
        self.__minute_hand = ClockHand(self.__minutes_values, system_time.minute)
        self.__second_hand = ClockHand(self.__seconds_values, system_time.second)

    def synchronize(self, time_value: ClockTime) -> None:
        self.__hour_hand = ClockHand(self.__hours_values, time_value.hour)
        self.__minute_hand = ClockHand(self.__minutes_values, time_value.minute)
        self.__second_hand = ClockHand(self.__seconds_values, time_value.second)

    def synchronize_with_system_time(self) -> None:
        self.synchronize(self.__time_service.get_system_time())

    def tick(self) -> ClockTime:
        previous_second = self.__second_hand.current_value
        previous_minute = self.__minute_hand.current_value

        self.__second_hand.move_forward()

        if previous_second == 59:
            self.__minute_hand.move_forward()

            if previous_minute == 59:
                self.__hour_hand.move_forward()

        return self.get_current_time()

    def move_backward_one_second(self) -> ClockTime:
        previous_second = self.__second_hand.current_value
        previous_minute = self.__minute_hand.current_value

        self.__second_hand.move_backward()

        if previous_second == 0:
            self.__minute_hand.move_backward()

            if previous_minute == 0:
                self.__hour_hand.move_backward()

        return self.get_current_time()

    def get_current_time(self) -> ClockTime:
        return ClockTime(
            hour=self.__hour_hand.current_value,
            minute=self.__minute_hand.current_value,
            second=self.__second_hand.current_value,
        )

    @staticmethod
    def __build_circular_values(start: int, end: int) -> CircularDoublyLinkedList[int]:
        values = CircularDoublyLinkedList[int]()
        for value in range(start, end + 1):
            values.append(value)
        return values
