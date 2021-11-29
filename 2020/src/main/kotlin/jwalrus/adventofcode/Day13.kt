package jwalrus.adventofcode

import jwalrus.adventofcode.util.load


object Day13 {

    fun List<String>.parse(): Pair<Int, List<Int?>> =
        get(0).toInt() to get(1).split(",").map(String::toIntOrNull)

    fun List<String>.parse2(): List<Pair<Int, Int>> =
            get(1).split(",")
                .mapIndexed { ix, s -> ix to s }
                .filter { it.second != "x" }
                .map { (ix, x) -> ix to x.toInt() }

    fun bus(time: Int, busses: List<Int?>): Int?
        = busses.filterNotNull().firstOrNull { time % it == 0 }

    fun Pair<Int, List<Int?>>.part1() = generateSequence(first, Int::inc)
        .map { it to bus(it, second) }
        .first { it.second != null }
        .let { (time,busId) -> (time - first) * busId!! }

    /**
     * Assist goes to kotlin slack's #advent-of-code channel
     */
    fun List<Pair<Int, Int>>.part2(): Long {
        // example: (0, 7), (1,5), (2,3)
        // t = 0,  hits: (0,7)
        // t = 7,  hits: (0,7), (2,3)
        // t = 28, hits: (0,7), (2,3)
        // t = 49, hits: (0,7), (1,5), (2,3)
        tailrec fun go(time: Long): Long {
            val hits = filter { (ix, busId) -> (time + ix) % busId == 0L }
            return if (hits.size == this.size) time
                   else go(time + hits.fold(1L) { acc, x -> acc * x.second })
        }

        return go(0)
    }
}

fun main() = Day13.run {

    val sample = load("day13_data_sample.txt")
    val challenge = load("day13_data.txt")

    println(sample.parse().part1()) // 295
    println(challenge.parse().part1()) // 3997
    println(sample.parse2().part2()) // 1068781
    println(challenge.parse2().part2()) // 500033211739354
}