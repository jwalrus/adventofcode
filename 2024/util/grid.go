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

func (p Point) Add(o Point) Point {
	return Point{
		R: p.R + o.R,
		C: p.C + o.C,
	}
}
