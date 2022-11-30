package main

import "testing"

func TestFoo(t *testing.T) {
	got := 2 + 2
	want := 4

	if got != want {
		t.Errorf("Expected %d, but got %d", want, got)
	}
}
