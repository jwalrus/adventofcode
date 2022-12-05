package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	fmt.Println("Day 05, 2022")
	fmt.Println("------------")

	raw, _ := os.ReadFile(os.Args[1])
	txt := strings.Split(string(raw), "\n\n")
	crates := parseCrates(strings.Split(txt[0], "\n"))
	instructions := strings.Split(txt[1], "\n")

	fmt.Printf("part1: %s\n", move(crates, instructions, reverse))                            // HNSNMTLHQ
	fmt.Printf("part2: %s\n", move(crates, instructions, func(s string) string { return s })) // RNVFPWQGH
}

func move(crates map[int]string, instructions []string, f func(s string) string) string {
	var n, from, to int
	result := ""

	for _, instruction := range instructions {
		_, _ = fmt.Sscanf(instruction, "move %d from %d to %d", &n, &from, &to)
		nw, toMove := mover(crates[from], n, f)
		crates[from] = nw
		crates[to] = crates[to] + toMove

		//for k, v := range crates {
		//	fmt.Println(k, v)
		//}
		//fmt.Println("---")
	}

	for i := 0; i < len(crates); i++ {
		v := crates[i+1]
		result = result + string(v[len(v)-1])
	}

	return result
}

func mover(s string, n int, f func(string) string) (string, string) {
	m := len(s)
	if m < n {
		return "", s
	} else {
		return s[:m-n], f(s[m-n:])
	}
}

func parseCrates(raw []string) map[int]string {
	result := make(map[int]string)
	h := len(raw)
	w := len(raw[0])

	transposed := make([][]string, w)

	for j := 0; j < w; j++ {
		transposed[j] = make([]string, h)
		for i := 0; i < h; i++ {
			transposed[j][i] = string(raw[h-i-1][j])
		}
	}

	for i := range transposed {
		k := transposed[i][0]
		if k != " " {
			key, _ := strconv.Atoi(k)
			result[key] = strings.Trim(strings.Join(transposed[i][1:], ""), " ")
		}
	}

	return result
}

func reverse(s string) (result string) {
	for _, v := range s {
		result = string(v) + result
	}
	return
}
