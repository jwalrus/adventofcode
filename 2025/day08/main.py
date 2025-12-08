import heapq


class UnionFind:
    def __init__(self):
        self.parents = {}
        self.sizes = {}

    def make_set(self, x):
        if x not in self.parents:
            self.parents[x] = x
            self.sizes[x] = 1

    def find_set(self, x):
        if x == self.parents[x]:
            return x
        self.parents[x] = self.find_set(self.parents[x])
        return self.parents[x]

    def union_set(self, x, y):
        self.make_set(x)
        self.make_set(y)
        x = self.find_set(x)
        y = self.find_set(y)
        if x != y:
            self.parents[y] = x
            self.sizes[x] += self.sizes[y]


def distance(a, b):
    n = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
    return n ** 0.5


def part1(xs, num):
    n = len(xs)
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            distances.append((distance(xs[i], xs[j]), xs[i], xs[j]))
    heapq.heapify(distances)

    uf = UnionFind()

    for i in range(num):
        _, x, y = heapq.heappop(distances)
        uf.union_set(x, y)

    sizes = set()
    for k, v in uf.parents.items():
        if k == v:
            sizes.add(uf.sizes[k])

    heapq.heapify(list(sizes))

    result = 1
    for i in heapq.nlargest(3, sizes):
        result *= i

    return result


def part2(xs):
    n = len(xs)
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            distances.append((distance(xs[i], xs[j]), xs[i], xs[j]))
    heapq.heapify(distances)

    uf = UnionFind()

    while distances:
        _, x, y = heapq.heappop(distances)
        uf.union_set(x, y)
        if uf.sizes[x] == len(xs):
            print(x, y, uf.sizes[x])
            return x[0] * y[0]

    return -1


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "r") as fh:
        data = [tuple(map(int, l.split(","))) for l in fh.read().splitlines()]

    print("part 1:", part1(data, 1000))
    print("part 2:", part2(data))
