package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
)

func main() {
	lines := util.ReadInput(os.Args[1])
	topoMap := parse(lines)
	fmt.Println("part1:", run(topoMap, true))
	fmt.Println("part2:", run(topoMap, false))
}

func run(topoMap [][]int, part1 bool) int {
	result := 0
	nrow, ncol := len(topoMap), len(topoMap[0])

	for r := 0; r < nrow; r++ {
		for c := 0; c < ncol; c++ {
			if topoMap[r][c] == 0 {
				result += dfs(util.Point{R: r, C: c}, topoMap, part1)
			}
		}
	}

	return result
}

func dfs(start util.Point, xs [][]int, part1 bool) int {
	nr, nc := len(xs), len(xs[0])
	stack := make([]util.Point, 0)
	stack = append(stack, start)
	vecs := [4]util.Point{{R: 0, C: 1}, {R: 1, C: 0}, {R: 0, C: -1}, {R: -1, C: 0}}
	result := 0
	visited := make(map[util.Point]struct{})

	for len(stack) > 0 {
		cur := stack[0]
		stack = stack[1:]
		_, ok := visited[cur]
		if ok && part1 {
			continue
		}
		visited[cur] = struct{}{}

		value := xs[cur.R][cur.C]
		if value == 9 {
			result += 1
		}

		for _, vec := range vecs {
			candidate := cur.Add(vec)
			if candidate.R < 0 || candidate.C < 0 || candidate.R >= nr || candidate.C >= nc {
				continue
			}
			valueC := xs[candidate.R][candidate.C]
			if valueC-value != 1 {
				continue
			}
			stack = append(stack, candidate)
		}
	}

	return result
}

func parse(lines []string) [][]int {
	nr, nc := len(lines), len(lines[0])
	result := make([][]int, nr)
	for r := 0; r < nr; r++ {
		result[r] = make([]int, nc)
		for c := 0; c < nc; c++ {
			result[r][c] = int(lines[r][c] - '0')
		}
	}
	return result
}
