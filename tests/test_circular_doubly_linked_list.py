import unittest

from domain.structures.circular_doubly_linked_list import CircularDoublyLinkedList


class TestCircularDoublyLinkedList(unittest.TestCase):
    def setUp(self) -> None:
        self.values = CircularDoublyLinkedList[int]()
        for value in [0, 1, 2]:
            self.values.append(value)

    def test_forward_traversal_is_circular(self) -> None:
        result = list(self.values.iter_forward(steps=5))
        self.assertEqual(result, [0, 1, 2, 0, 1])

    def test_backward_traversal_is_circular(self) -> None:
        result = list(self.values.iter_backward(steps=5))
        self.assertEqual(result, [0, 2, 1, 0, 2])

    def test_nodes_keep_full_circular_links(self) -> None:
        head = self.values.head
        current = head

        for _ in range(self.values.size):
            self.assertIsNotNone(current.next)
            self.assertIsNotNone(current.prev)
            self.assertIs(current.next.prev, current)
            self.assertIs(current.prev.next, current)
            current = current.next

        self.assertIs(current, head)


if __name__ == "__main__":
    unittest.main()
