package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("Day 06, 2022")
	fmt.Println("------------")

	inputRaw, _ := os.ReadFile(os.Args[1])
	input := string(inputRaw)
	fmt.Printf("part1: %d\n", decoder(input, 4))  // 1480
	fmt.Printf("part2: %d\n", decoder(input, 14)) // 2746
}

func decoder(in string, k int) int {
	for i := k; i <= len(in); i++ {
		if unique(in[i-k:i], k) {
			return i
		}
	}
	panic("did not find start!")
}

func unique(sub string, k int) bool {
	set := make(map[rune]bool)
	for _, r := range sub {
		set[r] = true
	}
	return len(set) == k
}
