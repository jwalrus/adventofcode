package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
)

func main() {
	lines := util.ReadInput(os.Args[1])
	puzzle := make([][]rune, 0)
	for _, line := range lines {
		puzzle = append(puzzle, []rune(line))
	}
	frequencies := make(map[rune][]util.Point)

	for r, row := range puzzle {
		for c, val := range row {
			if val != '.' {
				if _, ok := frequencies[val]; !ok {
					frequencies[val] = make([]util.Point, 0)
				}
				frequencies[val] = append(frequencies[val], util.Point{R: r, C: c})
			}
		}
	}

	fmt.Println("part1:", part1(frequencies, puzzle))
	fmt.Println("part2:", part2(frequencies, puzzle))
}

func part1(frequencies map[rune][]util.Point, puzzle [][]rune) int {
	antiNodes := make(map[util.Point]int)

	for _, arr := range frequencies {
		for i := 0; i < len(arr); i++ {
			for j := i + 1; j < len(arr); j++ {
				a, b := arr[i], arr[j]
				dr, dc := b.R-a.R, b.C-a.C
				antiR, antiC := b.R+dr, b.C+dc
				if antiR >= 0 && antiC >= 0 && antiR < len(puzzle) && antiC < len(puzzle[0]) {
					antiNodes[util.Point{R: antiR, C: antiC}] += 1
				}

				dr, dc = a.R-b.R, a.C-b.C
				antiR, antiC = a.R+dr, a.C+dc
				if antiR >= 0 && antiC >= 0 && antiR < len(puzzle) && antiC < len(puzzle[0]) {
					antiNodes[util.Point{R: antiR, C: antiC}] += 1
				}
			}
		}
	}

	return len(antiNodes)
}

func part2(frequencies map[rune][]util.Point, puzzle [][]rune) int {
	antiNodes := make(map[util.Point]int)

	for _, arr := range frequencies {
		for i := 0; i < len(arr); i++ {
			for j := i + 1; j < len(arr); j++ {
				a, b := arr[i], arr[j]
				antiNodes[a] = 1
				antiNodes[b] = 1
				dr, dc := b.R-a.R, b.C-a.C
				antiR, antiC := b.R+dr, b.C+dc
				for antiR >= 0 && antiC >= 0 && antiR < len(puzzle) && antiC < len(puzzle[0]) {
					antiNodes[util.Point{R: antiR, C: antiC}] += 1
					antiR, antiC = antiR+dr, antiC+dc
				}

				dr, dc = a.R-b.R, a.C-b.C
				antiR, antiC = a.R+dr, a.C+dc
				for antiR >= 0 && antiC >= 0 && antiR < len(puzzle) && antiC < len(puzzle[0]) {
					antiNodes[util.Point{R: antiR, C: antiC}] += 1
					antiR, antiC = antiR+dr, antiC+dc
				}
			}
		}
	}

	return len(antiNodes)
}
