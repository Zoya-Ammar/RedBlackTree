# Red-Black Tree in Python

[![Tests](https://github.com/Zoya-Ammar/RedBlackTree/actions/workflows/tests.yml/badge.svg)](https://github.com/Zoya-Ammar/RedBlackTree/actions/workflows/tests.yml)

A from-scratch implementation of a self-balancing red-black binary search tree. The project demonstrates tree rotations, insertion rebalancing, parent-pointer maintenance, invariant validation, automated testing, and continuous integration.

## Features

- `O(log n)` insertion and lookup
- Left-left, left-right, right-left, and right-right rotation handling
- Duplicate numeric values
- Python membership checks such as `7 in tree`
- In-order iteration and traversal with node colors
- Built-in validation of every red-black invariant
- Pytest coverage across edge cases and 500 deterministic random insertions
- GitHub Actions test execution on Python 3.10–3.13

## Quick start

```python
from rbtree import Tree

tree = Tree(10)

for value in [5, 15, 1, 7, 12, 20]:
    tree.insert(value)

print(list(tree))       # [1, 5, 7, 10, 12, 15, 20]
print(12 in tree)       # True
print(tree.validate())  # True
```

## Run the tests

Requires Python 3.10 or newer.

```bash
python -m pip install -e ".[dev]"
pytest
```

## Red-black invariants tested

1. Every node is red or black.
2. The root is black.
3. Missing children are treated as black leaves.
4. A red node cannot have a red child.
5. Every path from a node to a missing leaf has the same black height.
6. The binary-search-tree ordering and parent pointers remain valid.

## Project structure

```text
.
├── rbtree.py
├── tests/
│   └── test_rbtree.py
├── pyproject.toml
└── .github/workflows/tests.yml
```

## Design notes

New nodes begin red. When insertion creates a red-red violation, the tree either recolors the parent and uncle or rotates around the grandparent. The root is restored to black after every insertion.

`Tree.validate()` is intentionally included so tests and users can verify the full set of structural and color invariants.

## License

This project is available under the MIT License.
