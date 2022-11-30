package util

import (
	"bufio"
	"log"
	"os"
)

func ReadInput(name string) []string {
	fs, err := os.Open(name)
	if err != nil {
		log.Fatalln(err)
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
