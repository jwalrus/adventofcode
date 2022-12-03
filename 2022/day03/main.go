package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2022/util"
	"os"
	"strings"
)

func main() {
	fmt.Println("Day 03, 2022")
	fmt.Println("------------")

	lines := util.ReadInput(os.Args[1])
	fmt.Printf("part1: %d\n", part1(lines)) // 8349
	fmt.Printf("part2: %d\n", part2(lines)) // 2681
}

func part1(lines []string) int {
	result := 0

	for _, line := range lines {
		cut := len(line) / 2
		left, right := line[:cut], line[cut:]
		for _, c := range left {
			if strings.Contains(right, string(c)) {
				result += priority(c)
				break
			}
		}
	}

	return result
}

func part2(lines []string) int {
	groups := util.Chunk(lines, 3)
	result := 0

	for _, group := range groups {
		result += priority(common(group))
	}

	return result
}

func common(xs []string) int32 {

	for _, c := range xs[0] {
		pred := func(s string) bool {
			return strings.Contains(s, string(c))
		}
		if util.All(xs[1:], pred) {
			return c
		}
	}
	panic("didn't find any common element")
}

func priority(x int32) int {
	if x >= 97 && x <= 122 {
		return int(x) - 96
	} else {
		return int(x) - 38
	}
}
