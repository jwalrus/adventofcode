package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
)

func main() {
	lines := util.ReadInput(os.Args[1])
	fmt.Println("part1:", run(lines, 0))
	fmt.Println("part1:", run(lines, 10000000000000))
}

func run(lines []string, scale int) int {
	result := 0

	for l := 0; l < len(lines); l = l + 4 {
		var ax, ay, bx, by, cx, cy int
		_, _ = fmt.Sscanf(lines[l+0], "Button A: X+%d, Y+%d", &ax, &ay)
		_, _ = fmt.Sscanf(lines[l+1], "Button B: X+%d, Y+%d", &bx, &by)
		_, _ = fmt.Sscanf(lines[l+2], "Prize: X=%d, Y=%d", &cx, &cy)

		// part1 vs part2
		cx, cy = cx+scale, cy+scale

		// cramers rule (https://en.wikipedia.org/wiki/Cramer%27s_rule)
		d := ax*by - bx*ay
		da := cx*by - bx*cy
		db := ax*cy - cx*ay

		// python: da == int(da), go: da == (da/d)*d
		if da == (da/d)*d && db == (db/d)*d {
			result += 3*da/d + db/d
		}
	}

	return result
}
