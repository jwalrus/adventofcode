package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
)

type void struct{}

type direction struct {
	dr int
	dc int
}

type coordinate struct {
	r int
	c int
}

type location struct {
	coord coordinate
	dir   direction
}

var member void

func main() {
	gmap := util.ReadInput(os.Args[1])
	fmt.Println("part1:", part1(gmap))
	fmt.Println("part2:", part2(gmap))
}

func part1(gmap []string) int {
	r, c := start(gmap)
	visited := make(map[coordinate]void)
	current := location{coordinate{r: r, c: c}, direction{dr: -1, dc: 0}}
	finished := false

	for {
		visited[current.coord] = member
		current, finished = advance(current, gmap)
		if finished {
			break
		}
	}

	return len(visited)
}

func part2(gmap []string) int {
	result := 0
	nrows, ncols := len(gmap), len(gmap[0])

	for row := 0; row < nrows; row++ {
		for col := 0; col < ncols; col++ {
			if gmap[row][col] == '.' {
				ngmap := make([]string, len(gmap))
				copy(ngmap, gmap)
				tmp := []rune(ngmap[row])
				tmp[col] = 'O'
				ngmap[row] = string(tmp)
				result += runner2(ngmap)
			}
		}
	}

	return result
}

func runner2(gmap []string) int {
	r, c := start(gmap)
	current1 := location{coordinate{r: r, c: c}, direction{dr: -1, dc: 0}}
	current2 := location{coordinate{r: r, c: c}, direction{dr: -1, dc: 0}}
	finished1, finished2 := false, false

	for {
		// turtle
		current1, finished1 = advance(current1, gmap)

		// hare
		current2, finished2 = advance(current2, gmap)
		current2, finished2 = advance(current2, gmap)

		if finished1 || finished2 {
			return 0
		}

		if current1 == current2 {
			return 1
		}
	}
}

func advance(cur location, gmap []string) (location, bool) {
	nrows, ncols := len(gmap), len(gmap[0])
	nr, nc := cur.coord.r+cur.dir.dr, cur.coord.c+cur.dir.dc
	if !(nr >= 0 && nr < nrows && nc >= 0 && nc < ncols) {
		return cur, true
	}

	if gmap[nr][nc] == '#' || gmap[nr][nc] == 'O' {
		dr, dc := turnRight(cur.dir.dr, cur.dir.dc)
		cur = location{cur.coord, direction{dr: dr, dc: dc}}
	} else {
		cur = location{coordinate{r: nr, c: nc}, cur.dir}
	}

	return cur, false
}

func start(gmap []string) (int, int) {
	for row := range gmap {
		for col := range gmap[row] {
			if gmap[row][col] == '^' {
				return row, col
			}
		}
	}
	return -1, -1
}

func turnRight(dr, dc int) (int, int) {
	switch {
	// > -- v
	case dr == 0 && dc == 1:
		return 1, 0
	// V -- <
	case dr == 1 && dc == 0:
		return 0, -1
	// < -- ^
	case dr == 0 && dc == -1:
		return -1, 0
	// ^ -- >
	case dr == -1 && dc == 0:
		return 0, 1
	}
	panic("missed a case!")
}
