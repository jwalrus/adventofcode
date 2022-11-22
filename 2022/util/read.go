package util

import (
	"fmt"
)

func Hello(name string) string {
	return fmt.Sprintf("Hello, %s!\n", name)
}

func ReadLines(filename string) []string {
	return make([]string, 0)
}
