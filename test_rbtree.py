import pytest
from rbtree import Tree


def inorder_values(node):
    if node is None:
        return []
    return inorder_values(node.left) + [node.value] + inorder_values(node.right)


def assert_bst_property(root):
    vals = inorder_values(root)
    assert vals == sorted(vals), f"BST property violated: {vals}"


def assert_root_black(tree):
    assert tree.root is not None
    assert tree.root.color == "black", "Root must be black"


def assert_no_red_red(node):
    """No red node can have a red child."""
    if node is None:
        return
    if node.color == "red":
        if node.left is not None:
            assert node.left.color == "black", f"Red-Red violation at {node.value} -> left {node.left.value}"
        if node.right is not None:
            assert node.right.color == "black", f"Red-Red violation at {node.value} -> right {node.right.value}"
    assert_no_red_red(node.left)
    assert_no_red_red(node.right)


def assert_parent_pointers(node):
    """Child.parent should point back to node."""
    if node is None:
        return
    if node.left is not None:
        assert node.left.parent is node, f"Bad parent pointer: {node.left.value}.parent != {node.value}"
        assert node.left.direction == "left"
    if node.right is not None:
        assert node.right.parent is node, f"Bad parent pointer: {node.right.value}.parent != {node.value}"
        assert node.right.direction == "right"
    assert_parent_pointers(node.left)
    assert_parent_pointers(node.right)


@pytest.mark.parametrize(
    "values",
    [
        [5, 9, 6],
        [10, 5, 15, 1, 7, 12, 20],
        [5, 1, 9, 0, 3, 8, 6],
        [7, 3, 18, 10, 22, 8, 11, 26],
    ],
)
def test_insert_preserves_basic_rb_properties(values):
    t = Tree(values[0])
    for v in values[1:]:
        t.insert_and_balance(v)

    assert_root_black(t)
    assert_bst_property(t.root)
    assert_no_red_red(t.root)
    assert_parent_pointers(t.root)


def test_insert_many_random_values():
    t = Tree(50)
    values = list(range(0, 100))
    # deterministic shuffle without relying on random seed
    values = values[::2] + values[1::2]
    for v in values:
        if v != 50:
            t.insert_and_balance(v)

    assert_root_black(t)
    assert_bst_property(t.root)
    assert_no_red_red(t.root)
