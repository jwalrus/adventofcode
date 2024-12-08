package util

var Vectors = [8][2]int{
	{0, 1},
	{0, -1},
	{-1, 0},
	{1, 0},
	{-1, 1},
	{1, -1},
	{-1, -1},
	{1, 1},
}

type Point struct {
	R int
	C int
}

func (p Point) add(dr, dc int) Point {
	return Point{
		R: p.R + dr,
		C: p.C + dc,
	}
}
