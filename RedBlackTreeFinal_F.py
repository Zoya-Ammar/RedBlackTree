"""A red-black tree implementation with insertion and validation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Literal, Optional

Color = Literal["red", "black"]
Direction = Literal["left", "right", "root"]


@dataclass
class Node:
    """A node stored in :class:`Tree`."""

    value: int | float
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    direction: Direction = "root"
    parent: Optional["Node"] = None
    color: Color = "red"

    def set_right(self, value: int | float) -> "Node":
        self.right = Node(value, direction="right", parent=self)
        return self.right

    def set_left(self, value: int | float) -> "Node":
        self.left = Node(value, direction="left", parent=self)
        return self.left

    def __repr__(self) -> str:
        return f"Node(value={self.value!r}, color={self.color!r})"


class Tree:
    """A red-black binary search tree.

    Duplicate values are allowed and are inserted into the right subtree.
    Insertion and lookup are O(log n), while traversal is O(n).
    """

    def __init__(self, value: int | float):
        self.root = Node(value, color="black")

    @staticmethod
    def _color(node: Optional[Node]) -> Color:
        return "black" if node is None else node.color

    def add(self, item: int | float) -> Node:
        """Insert item as in a regular BST and return its new red node."""
        current = self.root

        while True:
            if item < current.value:
                if current.left is None:
                    return current.set_left(item)
                current = current.left
            else:
                if current.right is None:
                    return current.set_right(item)
                current = current.right

    def insert_and_balance(self, item: int | float) -> Node:
        """Insert item, restore all red-black properties, and return the node."""
        node = self.add(item)
        self.rebalance_insert(node)
        return node

    insert = insert_and_balance

    def rebalance_insert(self, node: Node) -> None:
        """Repair red-red violations following an insertion."""
        while node.parent is not None and node.parent.color == "red":
            parent = node.parent
            grandparent = parent.parent

            if grandparent is None:
                break

            if parent is grandparent.left:
                uncle = grandparent.right

                if self._color(uncle) == "red":
                    parent.color = "black"

                    assert uncle is not None
                    uncle.color = "black"

                    grandparent.color = "red"
                    node = grandparent
                else:
                    if node is parent.right:
                        node = parent
                        self._rotate_left(node)

                        parent = node.parent
                        assert parent is not None

                        grandparent = parent.parent
                        assert grandparent is not None

                    parent.color = "black"
                    grandparent.color = "red"
                    self._rotate_right(grandparent)
            else:
                uncle = grandparent.left

                if self._color(uncle) == "red":
                    parent.color = "black"

                    assert uncle is not None
                    uncle.color = "black"

                    grandparent.color = "red"
                    node = grandparent
                else:
                    if node is parent.left:
                        node = parent
                        self._rotate_right(node)

                        parent = node.parent
                        assert parent is not None

                        grandparent = parent.parent
                        assert grandparent is not None

                    parent.color = "black"
                    grandparent.color = "red"
                    self._rotate_left(grandparent)

        self.root.color = "black"
        self.root.parent = None
        self.root.direction = "root"

    def _replace_parent_link(self, old: Node, new: Node) -> None:
        parent = old.parent
        new.parent = parent

        if parent is None:
            self.root = new
            new.direction = "root"
        elif old is parent.left:
            parent.left = new
            new.direction = "left"
        else:
            parent.right = new
            new.direction = "right"

    def _rotate_left(self, pivot: Node) -> None:
        child = pivot.right

        if child is None:
            raise ValueError("A left rotation requires a right child")

        self._replace_parent_link(pivot, child)

        pivot.right = child.left

        if pivot.right is not None:
            pivot.right.parent = pivot
            pivot.right.direction = "right"

        child.left = pivot
        pivot.parent = child
        pivot.direction = "left"

    def _rotate_right(self, pivot: Node) -> None:
        child = pivot.left

        if child is None:
            raise ValueError("A right rotation requires a left child")

        self._replace_parent_link(pivot, child)

        pivot.left = child.right

        if pivot.left is not None:
            pivot.left.parent = pivot
            pivot.left.direction = "left"

        child.right = pivot
        pivot.parent = child
        pivot.direction = "right"

    def contains(self, item: int | float) -> bool:
        """Return whether item exists in the tree."""
        current: Optional[Node] = self.root

        while current is not None:
            if item == current.value:
                return True

            current = (
                current.left
                if item < current.value
                else current.right
            )

        return False

    def __contains__(self, item: object) -> bool:
        if not isinstance(item, (int, float)):
            return False

        return self.contains(item)

    def __iter__(self) -> Iterator[int | float]:
        stack: list[Node] = []
        current: Optional[Node] = self.root

        while stack or current is not None:
            while current is not None:
                stack.append(current)
                current = current.left

            current = stack.pop()
            yield current.value
            current = current.right

    def in_order_traversal(
        self,
        node: Optional[Node] = None,
    ) -> list[tuple[int | float, Color]]:
        """Return (value, color) pairs in sorted order."""
        start = self.root if node is None else node
        result: list[tuple[int | float, Color]] = []

        def visit(current: Optional[Node]) -> None:
            if current is None:
                return

            visit(current.left)
            result.append((current.value, current.color))
            visit(current.right)

        visit(start)
        return result

    def print(self) -> None:
        """Print the in-order traversal, one value and color per line."""
        for value, color in self.in_order_traversal():
            print(value, color)

    def validate(self) -> bool:
        """Raise AssertionError on an invariant violation; otherwise return True."""
        assert self.root.color == "black", "The root must be black"
        assert self.root.parent is None
        assert self.root.direction == "root"

        def check(
            node: Optional[Node],
            low: Optional[float],
            high: Optional[float],
        ) -> int:
            if node is None:
                return 1

            if low is not None:
                assert node.value >= low, "BST lower bound violated"

            if high is not None:
                assert node.value <= high, "BST upper bound violated"

            if node.left is not None:
                assert node.left.parent is node
                assert node.left.direction == "left"

            if node.right is not None:
                assert node.right.parent is node
                assert node.right.direction == "right"

            if node.color == "red":
                assert self._color(node.left) == "black"
                assert self._color(node.right) == "black"

            left_height = check(node.left, low, node.value)
            right_height = check(node.right, node.value, high)

            assert left_height == right_height, "Black-height mismatch"

            return left_height + (node.color == "black")

        check(self.root, None, None)
        return True
