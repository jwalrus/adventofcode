package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
	"strings"
)

func main() {
	lines := util.ReadInput(os.Args[1])
	rocks := parse(lines)
	fmt.Println("part1:", run(rocks, 25))
	fmt.Println("part1:", run(rocks, 75))
}

func run(rocks []int, n int) int {
	result := 0
	cache := make(map[[2]int]int)
	for _, rock := range rocks {
		result += work(rock, n, cache)
	}
	return result
}

func work(rock int, n int, cache map[[2]int]int) int {
	if n == 0 {
		return 1
	}

	value, ok := cache[[2]int{rock, n}]
	if ok {
		return value
	}

	count := 0
	for _, r := range mutate(rock) {
		count += work(r, n-1, cache)
	}

	cache[[2]int{rock, n}] = count

	return count
}

func mutate(x int) []int {
	result := make([]int, 0)

	switch {
	case x == 0:
		result = append(result, 1)
	case numDigits(x)%2 == 0:
		result = append(result, split(x)...)
	default:
		result = append(result, x*2024)
	}

	return result
}

func numDigits(x int) int {
	count := 0
	for x > 0 {
		x /= 10
		count++
	}
	return count
}

func split(x int) []int {
	n := numDigits(x)
	cut := n / 2
	y := 1
	left := x
	right := 0

	for i := 0; i < cut; i++ {
		right += (x % 10) * y
		y *= 10
		x /= 10
	}

	left = (left - right) / y

	return []int{left, right}
}

func parse(lines []string) []int {
	result := make([]int, 0)
	for _, x := range strings.Split(lines[0], " ") {
		result = append(result, util.ToInt(x))
	}
	return result
}
