package jwalrus.adventofcode

import jwalrus.adventofcode.util.load

enum class Direction { E, SE, SW, W, NW, NE }
enum class Color { B, W }

data class HexPoint(val x: Int, val y: Int, val z: Int) {
    operator fun plus(o: HexPoint): HexPoint = HexPoint(x + o.x, y + o.y, z + o.z)
    fun neighbor(d: Direction): HexPoint = this + when (d) {
        Direction.E -> HexPoint(1, 1, 0)
        Direction.SE -> HexPoint(1, 0, -1)
        Direction.SW -> HexPoint(0, -1, -1)
        Direction.W -> HexPoint(-1, -1, 0)
        Direction.NW -> HexPoint(-1, 0, 1)
        Direction.NE -> HexPoint(0, 1, 1)
    }
}

typealias Floor = MutableMap<HexPoint, Color>

object Day24 {

    private fun follow(instruction: String, floor: Floor): Unit {

        tailrec fun go(s: String, hex: HexPoint): Unit {

            floor[hex] = floor.getOrDefault(hex, Color.W)
            Direction.values().forEach { d -> floor[hex.neighbor(d)] = floor.getOrDefault(hex.neighbor(d), Color.W) }

            return when {
                s.isEmpty() -> floor[hex] = if (floor.getOrDefault(hex, Color.W) == Color.W) Color.B else Color.W
                s.startsWith("e") -> go(s.drop(1), hex.neighbor(Direction.E))
                s.startsWith("w") -> go(s.drop(1), hex.neighbor(Direction.W))
                else -> go(s.drop(2), hex.neighbor(Direction.valueOf(s.take(2).toUpperCase())))
            }
        }

        go(instruction, HexPoint(0, 0, 0))
    }

    private fun evolve(floor: Floor): Floor {

        fun bn(hexPoint: HexPoint) = Direction.values()
            .count { floor.getOrDefault(hexPoint.neighbor(it), Color.W) == Color.B }

        val result: Floor = mutableMapOf()

        // grow map
        for (k in floor.keys) {
            for (d in Direction.values()) {
                val n = k.neighbor(d)
                result[n] = floor.getOrDefault(n, Color.W)
            }
        }

        // flip tiles
        for ((k, v) in result) {
            result[k] = when (bn(k)) {
                2 -> if (v == Color.W) Color.B else v
                0, 3, 4, 5, 6 -> if (v == Color.B) Color.W else v
                else -> v
            }
        }

        return result
    }

    fun List<String>.part1() = run {
        val floor: Floor = mutableMapOf()
        forEach { instruction -> follow(instruction, floor) }
        floor.values.count { it == Color.B }
    }

    fun List<String>.part2() = run {
        var floor: Floor = mutableMapOf()
        forEach { follow(it, floor) }
        repeat(100) { floor = evolve(floor) }
        floor.values.count { it == Color.B }
    }
}

fun main() = Day24.run {
    val sample = load("day24_data_sample.txt")
    val challenge = load("day24_data.txt")

    println(sample.part1()) // 10
    println(challenge.part1()) // 354
    println(sample.part2()) // 2208
    println(challenge.part2()) // 3608
}