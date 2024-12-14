package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"math"
	"os"
)

func main() {
	lines := util.ReadInput(os.Args[1])
	fmt.Println("part1:", part1(lines, 100, 101, 103))
	fmt.Println("part2:", part2(lines, 101, 103))
}

func part1(lines []string, n, nx, ny int) int {
	x, y, vx, vy := 0, 0, 0, 0
	midX, midY := nx/2, ny/2
	a, b, c, d := 0, 0, 0, 0

	for _, line := range lines {
		_, _ = fmt.Sscanf(line, "p=%d,%d v=%d,%d", &x, &y, &vx, &vy)
		x = mod(x+n*vx, nx)
		y = mod(y+n*vy, ny)
		if x < midX && y < midY {
			a += 1
		} else if x > midX && y < midY {
			b += 1
		} else if x < midX && y > midY {
			c += 1
		} else if x > midX && y > midY {
			d += 1
		}
	}

	return a * b * c * d
}

func part2(lines []string, nx, ny int) int {
	// trick from reddit
	// danger level will be low when robots form christmas tree
	// turns out it worked very well (just guessed it would be in first 10,000 iterations)
	// lucky break here ... not a general solution
	minScore := math.MaxInt
	minI := 0

	for i := 0; i < 10000; i++ {
		tmp := part1(lines, i, nx, ny)
		if tmp < minScore {
			minScore = tmp
			minI = i
		}
	}

	return minI
}

func mod(a, b int) int {
	return (a%b + b) % b
}
