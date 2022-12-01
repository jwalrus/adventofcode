package util

import (
	"bufio"
	"os"
)

func ReadInput(filename string) []string {
	fs, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer fs.Close()

	scanner := bufio.NewScanner(fs)
	scanner.Split(bufio.ScanLines)

	var result = make([]string, 0)

	for scanner.Scan() {
		result = append(result, scanner.Text())
	}

	return result
}
