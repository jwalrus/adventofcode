package main

import (
	"fmt"
	"github.com/jwalrus/adventofcode/2024/util"
	"os"
	"slices"
)

type block struct {
	offset int
	id     int
	size   int
}

func main() {
	puzzle := util.ReadInput(os.Args[1])[0]
	fmt.Println("partA:", partA(puzzle))
	fmt.Println("partB:", partB(puzzle))
}

func partA(puzzle string) int64 {
	files := make([]block, 0)
	spaces := make([]block, 0)
	final := make([]int, 0)
	fileId := 0
	offset := 0
	for i, r := range puzzle {
		n := int(r) - int('0')
		if i%2 == 0 {
			fileId = i / 2
			for j := 0; j < n; j++ {
				final = append(final, fileId)
				files = append(files, block{offset: offset, id: fileId, size: 1})
				offset += 1
			}
		} else {
			spaces = append(spaces, block{offset: offset, id: -1, size: n})
			for j := 0; j < n; j++ {
				final = append(final, -1)
				offset += 1
			}
		}
	}

	slices.Reverse(files)
	return compact(files, spaces, final)
}

func partB(puzzle string) int64 {
	files := make([]block, 0)
	spaces := make([]block, 0)
	final := make([]int, 0)
	fileId := 0
	offset := 0
	for i, r := range puzzle {
		n := int(r) - int('0')
		if i%2 == 0 {
			fileId = i / 2
			files = append(files, block{offset: offset, id: fileId, size: n})
			for j := 0; j < n; j++ {
				final = append(final, fileId)
				offset += 1
			}
		} else {
			spaces = append(spaces, block{offset: offset, id: -1, size: n})
			for j := 0; j < n; j++ {
				final = append(final, -1)
				offset += 1
			}
		}
	}

	slices.Reverse(files)
	return compact(files, spaces, final)
}

func compact(files, spaces []block, final []int) int64 {
	for _, file := range files {
		for s, space := range spaces {
			if space.offset < file.offset && file.size <= space.size {
				for i := 0; i < file.size; i++ {
					final[space.offset+i] = file.id
					final[file.offset+i] = -1
				}
				spaces[s] = block{offset: space.offset + file.size, id: -1, size: space.size - file.size}
				break
			}
		}
	}
	return score(final)
}

func score(disk []int) int64 {
	result := int64(0)

	for i, s := range disk {
		if s < 0 {
			continue
		}
		result = result + int64(s)*int64(i)
	}

	return result
}
