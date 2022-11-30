package main

import (
	"aoc2018/util"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func main() {
	part := os.Args[1]
	filename := os.Args[2]

	fmt.Println("Day 03, 2018")
	switch part {
	case "1":
		fmt.Printf("part 1: %v\n", part1(filename)) // 118539
	case "2":
		fmt.Printf("part 2: %v\n", part2(filename)) // #1270
	}
}

func part1(filename string) int {
	xs := util.ReadInput(filename)
	claims := parse(xs)
	fabric := fabricClaims(claims)

	result := 0
	for _, v := range fabric {
		if v > 1 {
			result++
		}
	}

	return result
}

func part2(filename string) string {
	xs := util.ReadInput(filename)
	claims := parse(xs)
	fabric := fabricClaims(claims)

	for _, claim := range claims {
		if allOnes(claim, fabric) {
			return claim.id
		}
	}

	panic("NOT FOUND!!")
}

type Pair struct {
	X int64
	Y int64
}

func (p Pair) add(other Pair) Pair {
	return Pair{
		X: p.X + other.X,
		Y: p.Y + other.Y,
	}
}

type Claim struct {
	id string
	p  Pair
	w  int64
	h  int64
}

func pi(s string) int64 {
	r, _ := strconv.ParseInt(s, 10, 64)
	return r
}

func parse(lines []string) []Claim {
	claims := make([]Claim, 0)

	regex := regexp.MustCompile("#(?P<id>\\d+) @ (?P<x>\\d+),(?P<y>\\d+): (?P<w>\\d+)x(?P<h>\\d+)")
	for _, line := range lines {
		match := regex.FindStringSubmatch(line)
		claim := Claim{
			id: match[1],
			p:  Pair{X: pi(match[2]), Y: pi(match[3])},
			w:  pi(match[4]),
			h:  pi(match[5]),
		}
		claims = append(claims, claim)
	}

	return claims
}

func claimToIdx(claim Claim) []Pair {
	result := make([]Pair, 0)

	var ix, iy int64

	for iy = 0; iy < claim.h; iy++ {
		for ix = 0; ix < claim.w; ix++ {
			p := Pair{X: ix, Y: iy}
			result = append(result, claim.p.add(p))
		}
	}

	return result
}

func fabricClaims(claims []Claim) map[Pair]int {
	result := make(map[Pair]int)

	for _, claim := range claims {
		for _, idx := range claimToIdx(claim) {
			result[idx] += 1
		}
	}

	return result
}

func allOnes(claim Claim, fabric map[Pair]int) bool {

	for _, idx := range claimToIdx(claim) {
		if fabric[idx] != 1 {
			return false
		}
	}

	return true
}
