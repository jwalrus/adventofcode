package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2022/util"
	"os"
)

const (
	Rock    = 1
	Paper   = 2
	Scissor = 3
	Lose    = 0
	Draw    = 3
	Win     = 6
)

func main() {
	fmt.Println("Day 02, 2022")
	fmt.Println("------------")

	lines := util.ReadInput(os.Args[1])
	fmt.Printf("part1: %d\n", part1(lines)) // 11150
	fmt.Printf("part2: %d\n", part2(lines)) // 8295
}

func part1(lines []string) int {
	// A Rock, B Paper, C Scissor
	// X Rock, Y Paper, Z Scissor
	scores := map[string]int{
		"A X": Draw + Rock,
		"B X": Lose + Rock,
		"C X": Win + Rock,
		"A Y": Win + Paper,
		"B Y": Draw + Paper,
		"C Y": Lose + Paper,
		"A Z": Lose + Scissor,
		"B Z": Win + Scissor,
		"C Z": Draw + Scissor,
	}

	return calc(lines, scores)
}

func part2(lines []string) int {
	// A Rock, B Paper, C Scissor
	// X Lose, Y Draw, Z Win
	scores := map[string]int{
		"A X": Lose + Scissor,
		"B X": Lose + Rock,
		"C X": Lose + Paper,
		"A Y": Draw + Rock,
		"B Y": Draw + Paper,
		"C Y": Draw + Scissor,
		"A Z": Win + Paper,
		"B Z": Win + Scissor,
		"C Z": Win + Rock,
	}

	return calc(lines, scores)
}

func calc(games []string, scores map[string]int) int {
	result := 0

	for _, game := range games {
		result += scores[game]
	}

	return result
}
