package jwalrus.adventofcode

import jwalrus.adventofcode.util.createVector
import jwalrus.adventofcode.util.load

class SledMap(private val map: List<String>) {

    private val height = map.size
    private val width = map.first().length

    // for some reason I decided to switch the usual meaning of x and y ¯\_(ツ)_/¯
    private fun treesOnPath(down: Int, right: Int): Long = createVector(Pair(0, 0), Pair(down, right))
        .takeWhile { (x, _) -> x < height }
        .fold(0L) { acc, (x, y) -> acc + if (map[x][y % width] == '#') 1 else 0 }

    fun part1(down: Int, right: Int): Long = treesOnPath(down, right)

    fun part2(slopes: List<Pair<Int, Int>>): Long = slopes.fold(1L) { acc, (x,y) -> acc * treesOnPath(x, y) }
}

fun main() {
    val sample = load("day03_data_sample.txt")
    val challenge = load("day03_data.txt")

    println(SledMap(sample).part1(1, 3)) // 7
    println(SledMap(challenge).part1(1, 3)) // 289

    val slopes = listOf(
        1 to 1,
        1 to 3,
        1 to 5,
        1 to 7,
        2 to 1
    )

    println(SledMap(sample).part2(slopes)) // 336
    println(SledMap(challenge).part2(slopes)) // 5_522_401_584
}