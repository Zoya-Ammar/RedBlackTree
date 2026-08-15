import random

import pytest

from rbtree import Tree


@pytest.mark.parametrize(
    "values",
    [
        [5, 9, 6],                    # Right-left rotation
        [10, 5, 1],                   # Left-left rotation
        [10, 5, 7],                   # Left-right rotation
        [10, 15, 20],                 # Right-right rotation
        [10, 5, 15, 1, 7, 12, 20],
        [7, 3, 18, 10, 22, 8, 11, 26],
    ],
)
def test_insert_preserves_all_red_black_properties(values):
    tree = Tree(values[0])

    for value in values[1:]:
        tree.insert(value)

    assert tree.validate()
    assert list(tree) == sorted(values)


def test_many_deterministic_random_insertions():
    values = list(range(500))
    random.Random(2026).shuffle(values)

    tree = Tree(values[0])

    for value in values[1:]:
        tree.insert(value)
        assert tree.validate()

    assert list(tree) == sorted(values)


def test_duplicate_values_are_supported():
    tree = Tree(5)

    for value in [5, 5, 3, 7, 5]:
        tree.insert(value)

    assert tree.validate()
    assert list(tree) == [3, 5, 5, 5, 5, 7]


def test_lookup_and_python_membership():
    tree = Tree(10)

    for value in [4, 14, 2, 7]:
        tree.insert(value)

    assert tree.contains(7)
    assert 14 in tree
    assert 99 not in tree
    assert "10" not in tree


def test_in_order_traversal_includes_color_metadata():
    tree = Tree(5)
    tree.insert(9)
    tree.insert(6)

    traversal = tree.in_order_traversal()

    assert [value for value, _ in traversal] == [5, 6, 9]
    assert {color for _, color in traversal} <= {"red", "black"}
