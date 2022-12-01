package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2022/util"
	"os"
	"sort"
	"strconv"
)

func main() {
	fmt.Println("Day 01, 2022")
	fmt.Println("------------")

	lines := util.ReadInput(os.Args[1])
	fmt.Printf("part1: %d\n", part1(lines)) // 69795
	fmt.Printf("part2: %d\n", part2(lines)) // 208437
}

func part1(lines []string) int {
	counts := calorieCounts(lines)
	return counts[0]
}

func part2(lines []string) int {
	counts := calorieCounts(lines)
	return util.SumInt(counts[:3])
}

func calorieCounts(lines []string) []int {
	blanks := len(util.Filter(lines, func(s string) bool { return s == "" }))
	counts := make([]int, blanks+1)
	ix := 0

	for _, line := range lines {
		switch line {
		case "":
			ix += 1
		default:
			x, _ := strconv.Atoi(line)
			counts[ix] += x
		}
	}

	sort.Slice(counts, func(i, j int) bool {
		return counts[i] > counts[j]
	})

	return counts
}
