package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
)

func main() {
	lines := util.ReadInput(os.Args[1])
	fmt.Println("part1:", run(lines, search1))
	fmt.Println("part2:", run(lines, search2))
}

func run(puzzle []string, f func(int, int, []string) int) int {
	result := 0
	for i, line := range puzzle {
		for j, _ := range line {
			result += f(i, j, puzzle)
		}
	}
	return result
}

func search1(row, col int, mat []string) int {
	vecs := [8][2]int{
		{-1, -1},
		{-1, 1},
		{1, -1},
		{1, 1},
		{0, 1},
		{0, -1},
		{1, 0},
		{-1, 0},
	}

	nrow, ncol := len(mat), len(mat[0])
	sum := 0

	for _, vec := range vecs {
		dx, dy := vec[0], vec[1]
		for i, j, d := row, col, 0; i >= 0 && i < nrow && j >= 0 && j < ncol && d < 4; i, j, d = i+dy, j+dx, d+1 {

			r := mat[i][j]

			if d == 0 && r != 'X' {
				break
			} else if d == 1 && r != 'M' {
				break
			} else if d == 2 && r != 'A' {
				break
			} else if d == 3 {
				if r != 'S' {
					break
				} else {
					sum += 1
				}
			}
		}
	}

	return sum
}

func search2(row, col int, mat []string) int {
	nrow, ncol := len(mat), len(mat[0])
	sum := 0

	if row == 0 || col == 0 || row == nrow-1 || col == ncol-1 {
		return sum
	}

	if mat[row][col] != 'A' {
		return sum
	}

	if ((mat[row-1][col-1] == 'M' && mat[row+1][col+1] == 'S') || (mat[row-1][col-1] == 'S' && mat[row+1][col+1] == 'M')) &&
		((mat[row-1][col+1] == 'M' && mat[row+1][col-1] == 'S') || (mat[row-1][col+1] == 'S' && mat[row+1][col-1] == 'M')) {
		sum += 1
	}

	return sum
}
