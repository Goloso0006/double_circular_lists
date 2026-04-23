from __future__ import annotations

from domain.entities.time_node import TimeNode
from domain.structures.circular_doubly_linked_list import CircularDoublyLinkedList


class ClockHand:
    """Representa una manecilla que navega sobre una lista circular doble."""

    def __init__(self, values: CircularDoublyLinkedList[int], initial_value: int) -> None:
        self.__values = values
        self.__current: TimeNode[int] = values.find_node(initial_value)

    def move_forward(self) -> int:
        next_node = self.__current.next
        if next_node is None:
            raise RuntimeError("Invalid hand state.")
        self.__current = next_node
        return self.__current.value

    def move_backward(self) -> int:
        prev_node = self.__current.prev
        if prev_node is None:
            raise RuntimeError("Invalid hand state.")
        self.__current = prev_node
        return self.__current.value

    @property
    def current_value(self) -> int:
        return self.__current.value
