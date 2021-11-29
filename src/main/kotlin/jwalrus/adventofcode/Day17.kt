package jwalrus.adventofcode

import jwalrus.adventofcode.util.load

object Day17 {

    data class Point(val x: Int, val y: Int, val z: Int = 0, val w: Int = 0) {
        val neighbors: Collection<Point> by lazy { neighborhoodOf(this) }
        operator fun plus(other: Point) = Point(x + other.x, y + other.y, z + other.z, w + other.w)
    }

    fun List<String>.parse(): List<Point> = flatMapIndexed { row: Int, s: String ->
        s.trim().mapIndexed { col, c -> col to c }
            .filter { (_, v) -> v == '#' }
            .map { (col, _) -> Point(col, row) }
    }

    fun neighborhoodOf(p: Point) = (-1..1).flatMap { x ->
        (-1..1).flatMap { y ->
            (-1..1).flatMap { z ->
                (-1..1).map { w -> Point(x, y, z, w) }
            }
        }
    }.filter { it != Point(0, 0, 0, 0) }.map { p + it }

    fun runCycle(active: Set<Point>): Set<Point> {
        val map = mutableMapOf<Point, Int>()
        active.forEach { a ->
            a.neighbors.forEach {
                map[it] = map.getOrDefault(it, 0) + 1
            }
        }

        return map.filter { (p, i) -> (i == 3) || (i == 2 && p in active) }.keys
    }

    fun List<String>.part1() = run {
        var active = this.parse().toSet()
        for (i in 1..6) active = runCycle(active)
        active.size
    }

    fun List<String>.part2() = run {
        this.part1()
    }
}

fun main() = Day17.run {

    val sample = load("day17_data_sample.txt").also(::println)
    val challenge = load("day17_data.txt")


    println(sample.part1()) // ???
    println(challenge.part1()) // ???
    println(sample.part2()) // 848
    println(challenge.part2()) // 1524
}