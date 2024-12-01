package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
	"slices"
	"strconv"
	"strings"
)

func part1(left []int, right []int) int {
	sum := 0
	for i := 0; i < len(left); i++ {
		l, r := left[i], right[i]
		if l < r {
			l, r = r, l
		}
		sum += l - r
	}
	return sum
}

func part2(left []int, right []int) int {
	counts := make(map[int]int)
	for _, v := range right {
		counts[v] += 1
	}
	result := 0
	for _, k := range left {
		result += k * counts[k]
	}
	return result
}

func main() {
	lines := util.ReadInput(os.Args[1])
	left, right := make([]int, 0), make([]int, 0)
	for _, line := range lines {
		nums := strings.Split(line, "   ")
		x, _ := strconv.Atoi(nums[0])
		y, _ := strconv.Atoi(nums[1])
		left = append(left, x)
		right = append(right, y)
	}

	slices.Sort(left)
	slices.Sort(right)

	fmt.Println("part 1:", part1(left, right))
	fmt.Println("part 2:", part2(left, right))
}
