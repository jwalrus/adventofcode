package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"math"
	"os"
)

type void struct{}

var member void

type point struct {
	R int
	C int
}

type direction struct {
	dr int
	dc int
}

func main() {
	lines := util.ReadInput(os.Args[1])
	start, end := startEnd(lines)
	fromStart := part1(lines, start, end, direction{dr: 0, dc: 1})
	fmt.Println("part1:", fromStart[end])
	fromEnd := part1(lines, end, start, direction{dr: -1, dc: 0})

	best := 0
	for k, v := range fromStart {
		vv := fromEnd[k]
		if v == vv {
			best += 1
		}
	}
	fmt.Println(best)
}

func part1(maze []string, start, end point, d direction) map[point]int {
	distances := make(map[point]int)
	directions := make(map[point]direction)
	visited := make(map[point]void)

	for r, row := range maze {
		for c, val := range row {
			if val != '#' {
				p := point{R: r, C: c}
				distances[p] = math.MaxInt
			}
		}
	}
	distances[start] = 0
	directions[start] = d

	cur := start
	for cur != end {
		// find point with the shortest distance that hasn't been visited
		minV := math.MaxInt
		for k, v := range distances {
			_, ok := visited[k]
			if v < minV && !ok {
				cur = k
				minV = v
			}
		}

		visited[cur] = member
		d, ok := directions[cur]
		if !ok {
			panic("alksdjflks")
		}

		straight := point{R: cur.R + d.dr, C: cur.C + d.dc}
		clockwise, clockwiseD := rotateClockwise(cur, d)
		counterclockwise, counterD := rotateCounterClockwise(cur, d)

		mStraight := point{R: straight.R, C: straight.C}
		_, ok = distances[mStraight]
		_, vt := visited[mStraight]
		if ok && !vt {
			distances[mStraight] = minV + 1
			directions[mStraight] = d
		}

		mClockwise := point{R: clockwise.R, C: clockwise.C}
		_, ok = distances[mClockwise]
		_, vt = visited[mClockwise]
		if ok && !vt {
			distances[mClockwise] = minV + 1001
			directions[mClockwise] = clockwiseD
		}

		mCounter := point{R: counterclockwise.R, C: counterclockwise.C}
		_, ok = distances[mCounter]
		_, vt = visited[mCounter]
		if ok && !vt {
			distances[mCounter] = minV + 1001
			directions[mCounter] = counterD
		}
	}

	return distances
}

func startEnd(maze []string) (point, point) {
	SR, SC, ER, EC := 0, 0, 0, 0

	for r, row := range maze {
		for c, val := range row {
			if val == 'E' {
				ER, EC = r, c
			}
			if val == 'S' {
				SR, SC = r, c
			}
		}
	}

	return point{R: SR, C: SC}, point{R: ER, C: EC}
}

func rotateClockwise(p point, d direction) (point, direction) {
	if d.dr == 0 && d.dc == 1 {
		return point{R: p.R + 1, C: p.C}, direction{dr: 1, dc: 0}
	} else if d.dr == 0 && d.dc == -1 {
		return point{R: p.R - 1, C: p.C}, direction{dr: -1, dc: 0}
	} else if d.dr == -1 && d.dc == 0 {
		return point{R: p.R, C: p.C + 1}, direction{dr: 0, dc: 1}
	} else {
		return point{R: p.R, C: p.C - 1}, direction{dr: 0, dc: -1}
	}
}

func rotateCounterClockwise(p point, d direction) (point, direction) {
	if d.dr == 0 && d.dc == 1 {
		return point{R: p.R - 1, C: p.C}, direction{dr: -1, dc: 0}
	} else if d.dr == 0 && d.dc == -1 {
		return point{R: p.R + 1, C: p.C}, direction{dr: 1, dc: 0}
	} else if d.dr == -1 && d.dc == 0 {
		return point{R: p.R, C: p.C - 1}, direction{dr: 0, dc: -1}
	} else {
		return point{R: p.R, C: p.C + 1}, direction{dr: 0, dc: 1}
	}
}
