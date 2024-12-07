package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
	"strings"
)

type input struct {
	target   int
	operands []int
}

func main() {
	lines := util.ReadInput(os.Args[1])
	puzzle := parse(lines)
	fmt.Println("solution:", run(puzzle))
}

func run(puzzle []input) int {
	sum := 0
	for _, p := range puzzle {
		if backtrack(p.operands, p.target, -1) {
			sum += p.target
		}
	}
	return sum
}

func backtrack(xs []int, target int, acc int) bool {
	if len(xs) == 0 {
		return target == acc
	}
	// comment out last clause for part 1
	if acc == -1 {
		return backtrack(xs[1:], target, xs[0]) || backtrack(xs[1:], target, xs[0]*1) || backtrack(xs[1:], target, concat(xs[0], 0))
	}
	return backtrack(xs[1:], target, xs[0]+acc) || backtrack(xs[1:], target, xs[0]*acc) || backtrack(xs[1:], target, concat(acc, xs[0]))
}

func concat(x, y int) int {
	copyY := y
	lenY := 1
	for y > 0 {
		y /= 10
		lenY *= 10
	}
	return x*lenY + copyY
}

func parse(lines []string) []input {
	result := make([]input, len(lines))

	for i, line := range lines {
		l := strings.Split(line, ":")
		rr := strings.Split(strings.Trim(l[1], " "), " ")
		xs := make([]int, 0)
		for _, r := range rr {
			xs = append(xs, util.ToInt(r))
		}
		in := input{target: util.ToInt(l[0]), operands: xs}
		result[i] = in
	}

	return result
}
