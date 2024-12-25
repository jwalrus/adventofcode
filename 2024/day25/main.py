import sys


def main():
    with open(sys.argv[1]) as f:
        raw = f.read().split("\n\n")
    locks = [r.replace("\n", "") for r in raw if r[0] == "#"]
    keys = [r.replace("\n", "") for r in raw if r[0] != "#"]

    result = 0
    for lock in locks:
        for key in keys:
            if any(l == k and k == "#" for l, k in zip(lock, key)):
                continue
            else:
                result += 1
    print(result)


if __name__ == '__main__':
    main()