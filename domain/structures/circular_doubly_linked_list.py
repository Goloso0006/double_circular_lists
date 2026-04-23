from __future__ import annotations

from typing import Generic, Iterator, Optional, TypeVar

from domain.entities.time_node import TimeNode

T = TypeVar("T")


class CircularDoublyLinkedList(Generic[T]):
    """Lista doblemente enlazada circular para valores discretos del reloj."""

    def __init__(self) -> None:
        self.__head: Optional[TimeNode[T]] = None
        self.__size: int = 0

    @property
    def head(self) -> TimeNode[T]:
        if self.__head is None:
            raise ValueError("The list is empty.")
        return self.__head

    @property
    def size(self) -> int:
        return self.__size

    def append(self, value: T) -> TimeNode[T]:
        new_node = TimeNode(value)

        if self.__head is None:
            # El primer nodo se enlaza consigo mismo para mantener circularidad total.
            new_node.next = new_node
            new_node.prev = new_node
            self.__head = new_node
            self.__size = 1
            return new_node

        tail = self.__head.prev
        if tail is None:
            raise RuntimeError("Invalid circular list state.")

        new_node.prev = tail
        new_node.next = self.__head
        tail.next = new_node
        self.__head.prev = new_node
        self.__size += 1
        return new_node

    def iter_forward(self, steps: Optional[int] = None) -> Iterator[T]:
        if self.__head is None:
            return
            yield  # pragma: no cover

        current = self.__head
        yielded = 0

        while steps is None or yielded < steps:
            yield current.value
            next_node = current.next
            if next_node is None:
                raise RuntimeError("Invalid circular list state.")
            current = next_node
            yielded += 1

    def iter_backward(self, steps: Optional[int] = None) -> Iterator[T]:
        if self.__head is None:
            return
            yield  # pragma: no cover

        current = self.__head
        yielded = 0

        while steps is None or yielded < steps:
            yield current.value
            prev_node = current.prev
            if prev_node is None:
                raise RuntimeError("Invalid circular list state.")
            current = prev_node
            yielded += 1

    def find_node(self, target_value: T) -> TimeNode[T]:
        if self.__head is None:
            raise ValueError("Cannot search in an empty list.")

        current = self.__head
        for _ in range(self.__size):
            if current.value == target_value:
                return current
            next_node = current.next
            if next_node is None:
                raise RuntimeError("Invalid circular list state.")
            current = next_node

        raise ValueError(f"Value {target_value!r} not found in circular list.")
