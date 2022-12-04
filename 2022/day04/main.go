package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2022/util"
	"os"
	"strconv"
	"strings"
)

func main() {
	fmt.Println("Day 04, 2022")
	fmt.Println("------------")

	lines := util.ReadInput(os.Args[1])
	fmt.Printf("part1: %d\n", part1(lines)) // 556
	fmt.Printf("part2: %d\n", part2(lines)) // 876
}

func part1(lines []string) int {
	result := 0

	for _, line := range lines {
		a1, b1, a2, b2 := unpack(line)
		switch {
		case a1 <= a2 && a2 <= b2 && b2 <= b1:
			result += 1
		case a2 <= a1 && a1 <= b1 && b1 <= b2:
			result += 1
		}
	}

	return result
}

func part2(lines []string) int {
	result := 0

	for _, line := range lines {
		a1, b1, a2, b2 := unpack(line)
		switch {
		case a1 <= a2 && a2 <= b1:
			result += 1
		case a2 <= a1 && a1 <= b2:
			result += 1
		}
	}

	return result
}

func unpack(line string) (int, int, int, int) {
	ranges := strings.Split(line, ",")
	first := strings.Split(ranges[0], "-")
	second := strings.Split(ranges[1], "-")
	a1, _ := strconv.Atoi(first[0])
	b1, _ := strconv.Atoi(first[1])
	a2, _ := strconv.Atoi(second[0])
	b2, _ := strconv.Atoi(second[1])
	return a1, b1, a2, b2
}
