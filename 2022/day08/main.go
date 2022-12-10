package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2022/util"
	"os"
	"strconv"
)

func main() {
	lines := util.ReadInput(os.Args[1])
	trees := parse(lines)

	fmt.Printf("part1: %d\n", part1(trees)) // 1840
}

func part1(trees [][]int) int {
	result := 0

	for i, row := range trees {
		for j, tree := range row {
			if increasing(tree, above(i, j, trees)) ||
				increasing(tree, below(i, j, trees)) ||
				increasing(tree, left(i, j, trees)) ||
				increasing(tree, right(i, j, trees)) {

				//fmt.Println(i, j)
				result += 1
			}

			//fmt.Println(i, j, trees)
			//fmt.Println(increasing(above(i, j, trees)))
			//fmt.Println(increasing(below(i, j, trees)))
			//fmt.Println(increasing(left(i, j, trees)))
			//fmt.Println(right(i, j, trees))
		}
	}

	return result
}

func increasing(tree int, xs []int) bool {

	for _, x := range xs {
		if x >= tree {
			return false
		}
	}

	return true
}

func above(i, j int, trees [][]int) []int {
	result := make([]int, 0)

	for ii := 0; ii < i; ii++ {
		result = append(result, trees[ii][j])
	}

	return result
}

func below(i, j int, trees [][]int) []int {
	result := make([]int, 0)

	for ii := len(trees) - 1; ii > i; ii-- {
		result = append(result, trees[ii][j])
	}

	return result
}

func left(i, j int, trees [][]int) []int {
	result := make([]int, 0)

	for jj := 0; jj < j; jj++ {
		result = append(result, trees[i][jj])
	}

	return result
}

func right(i, j int, trees [][]int) []int {
	result := make([]int, 0)

	for jj := len(trees[0]) - 1; jj > j; jj-- {
		result = append(result, trees[i][jj])
	}

	return result
}

func parse(lines []string) [][]int {
	result := make([][]int, 0)

	for _, line := range lines {
		row := make([]int, 0)
		for _, i := range line {
			ii, _ := strconv.Atoi(string(i))
			row = append(row, ii)
		}
		result = append(result, row)
	}

	return result
}
