package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2022/util"
	"os"
)

func main() {
	filename := os.Args[1]
	fmt.Println(filename)
	fmt.Printf("Day01: %s", util.Hello("Advent of Code"))
	fmt.Printf("foo: %s\n", util.ReadLines(filename))
}
