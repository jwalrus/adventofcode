package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
	"strconv"
	"strings"
)

func main() {
	lines := util.ReadInput(os.Args[1])
	reports := make([][]int, len(lines))

	for row, line := range lines {
		xs := strings.Split(line, " ")
		report := reports[row]
		for _, x := range xs {
			y, _ := strconv.Atoi(x)
			report = append(report, y)
		}
		reports[row] = report
	}

	fmt.Println("part 1:", part1(reports))
	fmt.Println("part 2:", part2(reports))
}

func part1(reports [][]int) int {
	result := 0
	for _, report := range reports {
		if check(report) || check(reverse(report)) {
			result += 1
		}
	}
	return result
}

func part2(reports [][]int) int {
	result := 0
	for _, report := range reports {
		n := len(report)
		for i := 0; i < n; i++ {
			mod := make([]int, len(report))
			copy(mod, report)
			mod = append(mod[:i], mod[i+1:]...)
			if check(mod) || check(reverse(mod)) {
				result += 1
				break
			}
		}

	}

	return result
}

func reverse(xs []int) []int {
	result := make([]int, len(xs))
	for i, x := range xs {
		result[len(xs)-1-i] = x
	}
	return result
}

func check(xs []int) bool {
	for i := 1; i < len(xs); i++ {
		delta := xs[i] - xs[i-1]
		if delta < 1 || delta > 3 {
			return false
		}
	}
	return true
}
