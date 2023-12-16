import re


def find_destinations(seed, maps):
    results = []
    for map_ in maps:
        result = None
        for (dst, src, n) in map_:
            if src <= seed <= src + n:
                result = dst + (seed - src)
                break
        result = result if result is not None else seed
        results.append(result)
        seed = result
    return seed, results


def part1(seeds, maps):
    locations = []
    for seed in seeds:
        _, destinations = find_destinations(seed, maps)
        locations.append(destinations[-1])

    return min(locations)


def part2(seeds, maps):
    seed_pairs = [(s, l) for s, l in zip(seeds[::2], seeds[1::2])]
    seed_ranges = [(s, s + l) for s, l in seed_pairs]

    final_location_ranges = []

    for seed_range in seed_ranges:
        to_explore = [seed_range]
        next_ranges = []

        for map_ in maps:

            while to_explore:
                seed_start, seed_end = to_explore.pop()
                for (dst, src, n) in map_:
                    map_start, map_end = src, src + n
                    delta = dst - src

                    # case 1: seed interval is right of map interval
                    if seed_start >= map_end:
                        continue

                    # case 2: seed interval is left of map interval
                    if seed_end <= map_start:
                        continue

                    # case 3: seed interval within map interval
                    if map_start <= seed_start < seed_end <= map_end:
                        next_ranges.append((seed_start + delta, seed_end + delta))
                        break

                    # case 4: map interval within seed interval
                    if seed_start < map_start < map_end < seed_end:
                        to_explore.append((seed_start, map_start))
                        to_explore.append((map_end, seed_end))
                        next_ranges.append((map_start + delta, map_end + delta))
                        break

                    # case 5: left overlap
                    if seed_start < map_start < seed_end < map_end:
                        to_explore.append((seed_start, map_start))
                        next_ranges.append((map_start + delta, seed_end + delta))
                        break

                    # case 6: right overlap
                    if map_start < seed_start < map_end < seed_end:
                        to_explore.append((map_end, seed_end))
                        next_ranges.append((seed_start + delta, map_end + delta))
                        break

                else:
                    # if didn't find any overlapping ranges, then seed start and end map to self for next round
                    next_ranges.append((seed_start, seed_end))

            to_explore = next_ranges
            next_ranges = []

        final_location_ranges += to_explore
    return min(x[0] for x in final_location_ranges)


def main():
    with open(0) as f:
        raw_content = f.read()
        seeds, *maps = raw_content.split("\n\n")

    seeds = [int(r.group()) for r in re.finditer(r"\d+", seeds)]
    maps = [
        [
            x
            for line in map_.split("\n")
            if (x := [int(r.group()) for r in re.finditer(r"\d+", line)])
        ]
        for map_ in maps
    ]

    print("A:", part1(seeds, maps))  # 51,752,125
    print("B:", part2(seeds, maps))  # 12,634,632


if __name__ == "__main__":
    main()
