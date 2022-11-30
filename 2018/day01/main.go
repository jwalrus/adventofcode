package main

import (
	"aoc2018/util"
	"fmt"
	"os"
	"strconv"
)

func part1(filename string) int64 {

	lines := util.ReadInput(filename)

	var result int64 = 0
	for _, line := range lines {
		v, _ := strconv.ParseInt(line, 10, 64)
		result += v
	}

	return result
}

func part2(filename string) int64 {
	lines := util.ReadInput(filename)
	acc := map[int64]bool{0: true}

	var result int64 = 0

	for {
		for _, line := range lines {
			v, _ := strconv.ParseInt(line, 10, 64)
			result += v
			_, ok := acc[result]
			if ok {
				return result
			}
			acc[result] = true
		}
	}
}

func main() {
	filename := os.Args[1]
	fmt.Println("DAY 01, 2018")
	fmt.Printf("part 1: %d\n", part1(filename))
	fmt.Printf("part 2: %d\n", part2(filename))
}
