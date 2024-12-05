package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
	"slices"
	"strings"
)

type void struct{}

var member void

func main() {
	lines := util.ReadInput(os.Args[1])
	before, after, updates := parse(lines)
	fmt.Println("part1:", part1(before, after, updates))
	fmt.Println("part2:", part2(before, after, updates))
}

func part1(before, after map[int]map[int]void, updates [][]int) int {
	count := 0
	for _, update := range updates {
		if slices.IsSortedFunc(update, sorter(before, after)) {
			count += update[len(update)/2]
		}
	}
	return count
}

func part2(before, after map[int]map[int]void, updates [][]int) int {
	count := 0
	for _, update := range updates {
		if !slices.IsSortedFunc(update, sorter(before, after)) {
			slices.SortFunc(update, sorter(before, after))
			count += update[len(update)/2]
		}
	}
	return count
}

func sorter(before, after map[int]map[int]void) func(int, int) int {
	return func(a int, b int) int {
		_, ok := before[a][b]
		if ok {
			return 1
		}
		_, ok = after[a][b]
		if ok {
			return -1
		}
		return 0
	}
}

func parse(lines []string) (map[int]map[int]void, map[int]map[int]void, [][]int) {
	rules := make([]string, 0)
	updates := make([]string, 0)
	toggle := false

	for _, line := range lines {
		if line == "" {
			toggle = true
			continue
		}

		if toggle {
			updates = append(updates, line)
		} else {
			rules = append(rules, line)
		}
	}
	before, after := parseRules(rules)
	return before, after, parseUpdates(updates)
}

func parseRules(rules []string) (map[int]map[int]void, map[int]map[int]void) {
	before := make(map[int]map[int]void)
	after := make(map[int]map[int]void)

	for _, rule := range rules {
		rs := strings.Split(rule, "|")
		a, b := util.ToInt(rs[0]), util.ToInt(rs[1])

		if after[a] == nil {
			after[a] = make(map[int]void)
		}
		after[a][b] = member

		if before[b] == nil {
			before[b] = make(map[int]void)
		}
		before[b][a] = member
	}
	return before, after
}

func parseUpdates(updates []string) [][]int {
	result := make([][]int, len(updates))
	for i, rule := range updates {
		rs := strings.Split(rule, ",")
		xs := make([]int, 0)
		for _, r := range rs {
			xs = append(xs, util.ToInt(r))
		}
		result[i] = xs
	}
	return result
}
