package main

import (
	"aoc2018/util"
	"fmt"
	"os"
)

func counts(s string) (bool, bool) {
	acc := map[int32]int64{}

	twoResult := false
	threeResult := false

	for _, r := range s {
		acc[r] = acc[r] + 1
	}

	for _, v := range acc {
		if v == 2 {
			twoResult = true
		}

		if v == 3 {
			threeResult = true
		}
	}

	return twoResult, threeResult
}

func part1(filename string) int {

	twoAcc, threeAcc := 0, 0
	xs := util.ReadInput(filename)

	for _, x := range xs {
		two, three := counts(x)
		if two {
			twoAcc += 1
		}

		if three {
			threeAcc += 1
		}
	}

	return twoAcc * threeAcc
}

func diff(x string, y string) int {
	result := 0

	for i := range x {
		if x[i] != y[i] {
			result += 1
		}
	}

	return result
}

func withoutDiff(x string, y string) string {
	result := make([]uint8, 0)
	for i := range x {
		if x[i] == y[i] {
			result = append(result, x[i])
		}
	}
	return string(result)
}

func part2(filename string) string {
	xs := util.ReadInput(filename)

	for i, x := range xs {
		if i < len(xs) {
			for _, y := range xs[i+1:] {
				if diff(x, y) == 1 {
					return withoutDiff(x, y)
				}
			}
		}
	}

	return ""
}

func main() {
	filename := os.Args[1]
	fmt.Println("DAY 02, 2018!")
	fmt.Printf("part 1: %d\n", part1(filename)) // 7470
	fmt.Printf("part 2: %s\n", part2(filename)) // kqzxdenujwcstybmgvyiofrrd
}
