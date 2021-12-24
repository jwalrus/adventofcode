import copy
from dataclasses import dataclass

import pytest


class Tree:
    pass


@dataclass
class Node(Tree):
    id: int
    left: Tree
    right: Tree


@dataclass
class Leaf(Tree):
    id: int
    value: int


def build_tree(in_, *, start_id=0):
    def go(xs, next_id):
        if isinstance(xs, int):
            return next_id + 1, Leaf(id=next_id, value=xs)
        else:
            root_id, left = go(xs[0], next_id)
            next_id, right = go(xs[1], root_id + 1)
            return next_id, Node(id=root_id, left=left, right=right)

    return go(in_, start_id)


def merge_tree(left, right):
    new_tree = Node(id=-1, left=left, right=right)
    reindex(new_tree)
    return new_tree


def reindex(root, *, next_id=0):
    if isinstance(root, Leaf):
        root.id = next_id
        return next_id + 1
    else:
        next_id = reindex(root.left, next_id=next_id)
        root.id = next_id
        next_id = reindex(root.right, next_id=next_id + 1)
        return next_id


def find(root, *, id):
    if root.id == id:
        return root
    elif isinstance(root, Leaf):
        return None
    elif root.id < id:
        return find(root.right, id=id)
    else:
        return find(root.left, id=id)


def to_list(root):
    if isinstance(root, Leaf):
        return root.value
    else:
        return [to_list(root.left), to_list(root.right)]


def split(root, *, cutoff=10):
    if isinstance(root, Leaf):
        if root.value >= cutoff:
            if root.value % 2 == 0:
                new_node = Node(-3, Leaf(-1, root.value // 2),
                                Leaf(-2, root.value // 2))
            else:
                new_node = Node(-3, Leaf(-1, root.value // 2),
                                Leaf(-2, root.value // 2 + 1))
            return True, new_node
        else:
            return False, root

    found, new_left = split(root.left)
    if found:
        root.left = new_left
        return True, root

    found, new_right = split(root.right)
    if found:
        root.right = new_right
        return True, root

    return found, root


def explode(root, *, cutoff=4):
    def go(cur, depth):
        if isinstance(cur, Leaf):
            return False, cur
        else:
            if depth >= cutoff:
                left_neighbor = find(root, id=cur.left.id - 2)
                right_neighbor = find(root, id=cur.right.id + 2)
                if left_neighbor:
                    left_neighbor.value = cur.left.value + left_neighbor.value
                if right_neighbor:
                    right_neighbor.value = cur.right.value + right_neighbor.value
                return True, Leaf(-1, 0)
            else:
                found, new_left = go(cur.left, depth + 1)
                if found:
                    cur.left = new_left
                    return found, cur
                found, new_right = go(cur.right, depth + 1)
                if found:
                    cur.right = new_right
                    return found, cur
                return found, cur

    return go(root, depth=0)


def explode_snailfish(root):
    found_exp = True
    while found_exp:
        found_exp, root = explode(root)
        reindex(root)

    return root


def split_snailfish(root):
    found_split = True
    while found_split:
        found_split, root = split(root)
        reindex(root)
        # always explode after split
        explode_snailfish(root)

    return root


def magnitude(root):
    if isinstance(root, Leaf):
        return root.value
    return 3 * magnitude(root.left) + 2 * magnitude(root.right)


def part1(puzzle):
    graphs = [build_tree(x) for x in puzzle]
    root, *graphs = [g[1] for g in graphs]

    for graph in graphs:
        root = merge_tree(root, graph)
        root = explode_snailfish(root)
        root = split_snailfish(root)

    return magnitude(root)


def part2(puzzle):
    best = -1

    for i, left in enumerate(puzzle[:-1]):
        for right in puzzle[i + 1:]:
            for a, b in [(left, right), (right, left)]:
                _, a0 = build_tree(a)
                _, b0 = build_tree(b)

                root = merge_tree(a0, b0)
                root = explode_snailfish(root)
                root = split_snailfish(root)
                if magnitude(root) >= best:
                    best = magnitude(root)

    return best


class TestDay18:

    def test_puzzle_input(self, sample, puzzle):
        assert len(sample) == 10
        assert len(puzzle) == 100
        assert sample[0] == [[[0, [5, 8]], [[1, 7], [9, 6]]],
                             [[4, [1, 2]], [[1, 4], 2]]]

    def test_build_tree(self):
        in_ = [[[1, 2], 3], [4, 5]]
        leaf0 = Leaf(0, 1)
        leaf1 = Leaf(2, 2)
        node2 = Node(1, leaf0, leaf1)
        node3 = Node(3, node2, Leaf(4, 3))
        root = Node(5, node3, Node(7, Leaf(6, 4), Leaf(8, 5)))
        assert build_tree(in_) == (9, root)

    def test_merge_tree(self):
        _, left = build_tree([0, 1])
        _, right = build_tree([2, 3])
        root = merge_tree(left, right)
        assert root == Node(3,
                            Node(1, Leaf(0, 0), Leaf(2, 1)),
                            Node(5, Leaf(4, 2), Leaf(6, 3))
                            )

    def test_to_list(self):
        root = Node(3,
                    Node(1, Leaf(0, 0), Leaf(2, 1)),
                    Node(5, Leaf(4, 2), Leaf(6, 3))
                    )
        assert to_list(root) == [[0, 1], [2, 3]]

    def test_find(self):
        root = Node(3,
                    Node(1, Leaf(0, 0), Leaf(2, 1)),
                    Node(5, Leaf(4, 2), Leaf(6, 3))
                    )
        assert find(root, id=4 - 2) == Leaf(2, 1)
        assert find(root, id=2 + 2) == Leaf(4, 2)
        assert find(root, id=2 - 2) == Leaf(0, 0)
        assert find(root, id=-1) is None

    def test_merge_again(self):
        _, left = build_tree([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
        _, right = build_tree([1, 1])
        root = merge_tree(left, right)
        assert to_list(root) == [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]]

    def test_split(self):
        _, root = build_tree([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
        found, root = split(root)
        assert found
        assert to_list(root) == [[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]

        _, root = build_tree([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]])
        found, root = split(root)
        assert found
        assert to_list(root) == [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]

        _, root = build_tree([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]])
        found, root = split(root)
        assert not found
        assert to_list(root) == [[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]]

    def test_explode(self):
        _, root = build_tree([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])
        found, root = explode(root)
        assert found
        assert to_list(root) == [[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]]
        reindex(root)

        _, root = build_tree([[[[0, 7], 4], [7, [[8, 4], 9]]], [1, 1]])
        found, root = explode(root)
        assert found
        assert to_list(root) == [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]
        reindex(root)

        _, root = build_tree([[[[0, 7], 4], [15, [0, 13]]], [1, 1]])
        found, root = explode(root)
        assert not found
        assert to_list(root) == [[[[0, 7], 4], [15, [0, 13]]], [1, 1]]

    def test_part1_sample(self, sample):
        assert part1(sample) == 4140

    def test_part1(self, puzzle):
        assert part1(puzzle) == 4072

    def test_part2_sample(self, sample):
        assert part2(sample) == 3993

    def test_part2(self, puzzle):
        assert part2(puzzle) == 0


def parse_input(text):
    xs = [line.strip() for line in text.split("\n") if line != ""]
    return [eval(x) for x in xs]


@pytest.fixture(scope="module")
def puzzle():
    with open("day18.txt") as f:
        return parse_input(f.read())


@pytest.fixture(scope="module")
def sample():
    from textwrap import dedent
    return parse_input(dedent("""\
        [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
        [[[5,[2,8]],4],[5,[[9,9],0]]]
        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
        [[[[5,4],[7,7]],8],[[8,3],8]]
        [[9,3],[[9,9],[6,[4,9]]]]
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    """))
