package util

func All[T comparable](ts []T, predicate func(t T) bool) bool {
	for _, t := range ts {
		if !predicate(t) {
			return false
		}
	}
	return true
}

func Filter[T any](xs []T, predicate func(t T) bool) []T {
	result := make([]T, 0)

	for _, x := range xs {
		if predicate(x) {
			result = append(result, x)
		}
	}

	return result
}

func Chunk[T any](lines []T, n int) [][]T {
	result := make([][]T, 0)
	chunk := make([]T, 0)

	for i, line := range lines {
		if i%n == 0 && i != 0 {
			result = append(result, chunk)
			chunk = make([]T, 0)
		}
		chunk = append(chunk, line)
	}
	result = append(result, chunk)

	return result
}
