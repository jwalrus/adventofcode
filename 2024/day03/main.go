package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
	"regexp"
	"strconv"
)

func main() {
	lines := util.ReadInput(os.Args[1])
	fmt.Println("part1:", part1(lines))
	fmt.Println("part2:", part2(lines))
}

func part1(lines []string) int {
	result := 0
	re := regexp.MustCompile("mul\\((?P<first>\\d+),(?P<second>\\d+)\\)")
	for _, line := range lines {
		for _, match := range re.FindAllStringSubmatch(line, -1) {
			a, b := atoi(match[1]), atoi(match[2])
			result += a * b
		}
	}
	return result
}

func part2(lines []string) int {
	result := 0
	enabled := true
	re := regexp.MustCompile("do\\(\\)|don't\\(\\)|mul\\((?P<first>\\d+),(?P<second>\\d+)\\)")
	for _, line := range lines {
		for _, match := range re.FindAllStringSubmatch(line, -1) {
			if match[0] == "do()" {
				enabled = true
			} else if match[0] == "don't()" {
				enabled = false
			} else {
				if enabled {
					a, b := atoi(match[1]), atoi(match[2])
					result += a * b
				}
			}
		}
	}
	return result
}

func atoi(s string) int {
	i, _ := strconv.Atoi(s)
	return i
}
