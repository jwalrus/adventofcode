package util

func Filter[T any](xs []T, predicate func(t T) bool) []T {
	result := make([]T, 0)

	for _, x := range xs {
		if predicate(x) {
			result = append(result, x)
		}
	}

	return result
}
