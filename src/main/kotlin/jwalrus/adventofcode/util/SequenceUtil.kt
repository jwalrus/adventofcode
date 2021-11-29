package jwalrus.adventofcode.util

fun createVector(start: Pair<Int, Int>, direction: Pair<Int, Int>): Sequence<Pair<Int, Int>> =
    generateSequence(start) { it.first + direction.first to it.second + direction.second }