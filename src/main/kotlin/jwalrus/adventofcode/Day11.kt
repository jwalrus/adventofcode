package jwalrus.adventofcode

import jwalrus.adventofcode.util.createVector
import jwalrus.adventofcode.util.load

private typealias Seats = Map<Pair<Int, Int>, Day11.Coord>

object Day11 {

    val unitVectors = listOf(
        Pair(-1, -1), Pair(-1, 0), Pair(-1, 1), Pair(1, 1),
        Pair(1, 0), Pair(1, -1), Pair(0, -1), Pair(0, 1)
    )

    fun firstNeighbor(coord: Pair<Int, Int>, seats: Seats, direction: Pair<Int, Int>): Pair<Int, Int>? {
        return createVector(coord, direction).drop(1)
            .takeWhile { seats[it] != null }
            .filter { seats[it]?.value != "." }
            .firstOrNull()
    }

    fun adjacent(coord: Pair<Int, Int>, direction: Pair<Int, Int>): Pair<Int, Int> =
        coord.first + direction.first to coord.second + direction.second

    data class Coord(
        val coord: Pair<Int, Int>,
        val value: String
    ) {
        private val neighbors: Collection<Pair<Int, Int>> by lazy { unitVectors.map { adjacent(coord, it) } }
        private var fieldOfVision: Collection<Pair<Int, Int>> = emptyList()

        fun fieldOfVision(seats: Seats): Collection<Pair<Int, Int>> {
            if (fieldOfVision.isEmpty()) {
                fieldOfVision = unitVectors.mapNotNull { firstNeighbor(coord, seats, it) }
            }
            return fieldOfVision
        }

        fun occupiedNeighbors(seats: Seats): Int = neighbors.filter { seats[it]?.value == "#" }.count()
        fun occupiedVision(seats: Seats): Int = fieldOfVision(seats).filter { seats[it]?.value == "#" }.count()
    }

    private fun List<String>.toSeatMap(): Seats = flatMapIndexed { y, row ->
        row.mapIndexed { x, c -> (x to y) to Coord(x to y, "$c") }
    }.toMap()

    fun List<String>.part1(): Int {
        tailrec fun go(input: Seats): Int {
            val output = input.map { (k, v) ->
                k to when (v.occupiedNeighbors(input)) {
                    0 -> if (v.value == ".") Coord(k, ".") else Coord(k, "#")
                    1, 2, 3 -> Coord(k, v.value)
                    4, 5, 6, 7, 8 -> if (v.value == ".") Coord(k, ".") else Coord(k, "L")
                    else -> error("occupied neighbors > 8")
                }
            }.toMap()

            return if (input == output) output.values.count { it.value == "#" }
            else go(output)
        }
        return go(toSeatMap())
    }

    fun List<String>.part2(): Int {
        tailrec fun go(input: Seats): Int {
            val output = input.map { (k, v) ->
                k to when (v.occupiedVision(input)) {
                    0 -> if (v.value == ".") Coord(k, ".") else Coord(k, "#")
                    1, 2, 3, 4 -> Coord(k, v.value)
                    5, 6, 7, 8 -> if (v.value == ".") Coord(k, ".") else Coord(k, "L")
                    else -> error("occupied vision > 8")
                }
            }.toMap()

            return if (input == output) output.values.count { it.value == "#" }
            else go(output)
        }
        return go(toSeatMap())
    }
}

fun main(): Unit = Day11.run {

    val sample = load("day11_data_sample.txt")
    val challenge = load("day11_data.txt")

    println(sample.part1()) // 37
    println(challenge.part1()) // 2418
    println(sample.part2()) // 26
    println(challenge.part2()) // 2144
}