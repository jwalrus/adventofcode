package util

func SumInt(xs []int) int {
	result := 0

	for _, x := range xs {
		result += x
	}

	return result
}
