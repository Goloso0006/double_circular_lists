from __future__ import annotations

from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class TimeNode(Generic[T]):
    """Nodo para lista doblemente enlazada circular."""

    def __init__(self, value: T) -> None:
        self.__value: T = value
        self.__next: Optional["TimeNode[T]"] = None
        self.__prev: Optional["TimeNode[T]"] = None

    @property
    def value(self) -> T:
        return self.__value

    @property
    def next(self) -> Optional["TimeNode[T]"]:
        return self.__next

    @next.setter
    def next(self, node: "TimeNode[T]") -> None:
        self.__next = node

    @property
    def prev(self) -> Optional["TimeNode[T]"]:
        return self.__prev

    @prev.setter
    def prev(self, node: "TimeNode[T]") -> None:
        self.__prev = node
