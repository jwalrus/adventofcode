package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
)

type void struct{}

var member void

func main() {
	puzzle := util.ReadInput(os.Args[1])
	fmt.Println("part1:", run(puzzle, floodFill))
	fmt.Println("part2:", run(puzzle, floodFill2))
}

func run(puzzle []string, f func(util.Point, []string, map[util.Point]void) int) int {
	result := 0
	visited := make(map[util.Point]void)

	for r := 0; r < len(puzzle); r++ {
		for c := 0; c < len(puzzle[0]); c++ {
			result += f(util.Point{R: r, C: c}, puzzle, visited)
		}
	}
	return result
}

func floodFill(cur util.Point, puzzle []string, visited map[util.Point]void) int {
	nrow, ncol := len(puzzle), len(puzzle[0])
	vecs := [4]util.Point{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	plots, fences := 0, 0
	stack := make([]util.Point, 0)
	stack = append(stack, cur)

	for len(stack) > 0 {
		cur = stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		_, ok := visited[cur]
		if ok {
			continue
		}
		visited[cur] = member
		plots += 1

		// find neighbors
		for _, vec := range vecs {
			n := cur.Add(vec)
			if n.R < 0 || n.C < 0 || n.R >= nrow || n.C >= ncol {
				fences += 1
				continue
			}

			if puzzle[cur.R][cur.C] == puzzle[n.R][n.C] {
				stack = append(stack, n)
			} else {
				fences += 1
			}
		}

	}

	return plots * fences
}

func floodFill2(cur util.Point, puzzle []string, visited map[util.Point]void) int {
	nrow, ncol := len(puzzle), len(puzzle[0])
	vecs := [4]util.Point{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	plots, fences := 0, 0
	stack := make([]util.Point, 0)
	stack = append(stack, cur)
	found := make(map[util.Point]void)

	for len(stack) > 0 {
		cur = stack[len(stack)-1]
		stack = stack[:len(stack)-1]

		_, ok := visited[cur]
		if ok {
			continue
		}
		visited[cur] = member
		found[cur] = member
		plots += 1

		// find neighbors
		for _, vec := range vecs {
			n := cur.Add(vec)
			if n.R < 0 || n.C < 0 || n.R >= nrow || n.C >= ncol {
				fences += 1
				continue
			}

			if puzzle[cur.R][cur.C] == puzzle[n.R][n.C] {
				stack = append(stack, n)
			} else {
				fences += 1
			}
		}
	}

	return plots * corners(found)
}

func corners(points map[util.Point]void) int {
	if len(points) == 0 {
		return 0
	}
	result := 0

	for point := range points {
		_, up := points[point.Add(util.Point{R: -1})]
		_, rt := points[point.Add(util.Point{C: 1})]
		_, dn := points[point.Add(util.Point{R: 1})]
		_, lf := points[point.Add(util.Point{C: -1})]
		_, dul := points[point.Add(util.Point{R: -1, C: -1})]
		_, dur := points[point.Add(util.Point{R: -1, C: 1})]
		_, dll := points[point.Add(util.Point{R: 1, C: -1})]
		_, dlr := points[point.Add(util.Point{R: 1, C: 1})]
		// upper left
		if !up && !lf {
			result += 1
		}
		// upper right
		if !up && !rt {
			result += 1
		}
		// lower left
		if !dn && !lf {
			result += 1
		}
		// lower right
		if !dn && !rt {
			result += 1
		}
		// interior left/up
		if !dul && up && lf {
			result += 1
		}
		// interior left/down
		if !dur && up && rt {
			result += 1
		}
		// interior right/up
		if !dll && dn && lf {
			result += 1
		}
		// interior right/down
		if !dlr && dn && rt {
			result += 1
		}
	}

	return result
}
