package jwalrus.adventofcode

import jwalrus.adventofcode.util.load
import kotlin.math.abs

object Day12Part1 {
    fun List<String>.toInstructions(): List<Instruction> =
        map { Instruction(Code.valueOf("${it.first()}"), it.drop(1).toInt()) }


    enum class Code { N, E, S, W, R, L, F }
    data class Instruction(val code: Code, val value: Int)

    // directions N = 0, E = 90, S = 180, W = 270
    data class Boat(val x: Int, val y: Int, val direction: Int)

    fun forward(boat: Boat, distance: Int): Boat = when (boat.direction) {
        0 -> Boat(boat.x, boat.y + distance, boat.direction)
        90 -> Boat(boat.x + distance, boat.y, boat.direction)
        180 -> Boat(boat.x, boat.y - distance, boat.direction)
        270 -> Boat(boat.x - distance, boat.y, boat.direction)
        else -> error("unknown direction ${boat.direction}")
    }

    fun takeAction(boat: Boat, instruction: Instruction): Boat = when (instruction.code) {
        Code.N -> boat.copy(y = boat.y + instruction.value)
        Code.E -> Boat(boat.x + instruction.value, boat.y, boat.direction)
        Code.S -> Boat(boat.x, boat.y - instruction.value, boat.direction)
        Code.W -> Boat(boat.x - instruction.value, boat.y, boat.direction)
        Code.R -> Boat(boat.x, boat.y, (boat.direction + instruction.value) % 360)
        Code.L -> Boat(boat.x, boat.y, (boat.direction + (360 - instruction.value)) % 360)
        Code.F -> forward(boat, instruction.value)
    }

    fun List<Instruction>.part1(): Int =
        fold(Boat(0, 0, 90), { acc, instruction -> takeAction(acc, instruction) })
            .let { boat -> abs(boat.x) + abs(boat.y) }
}

object Day12Part2 {
    fun List<String>.toInstructions(): List<Instruction> =
        map { Instruction(Code.valueOf("${it.first()}"), it.drop(1).toInt()) }


    enum class Code { N, E, S, W, R, L, F }
    data class Instruction(val code: Code, val value: Int)
    data class Waypoint(val x: Int, val y: Int)
    // directions N = 0, E = 90, S = 180, W = 270
    data class Boat(val x: Int, val y: Int, val waypoint: Waypoint)

    fun rotate(waypoint: Waypoint, direction: Int): Waypoint = when (direction) {
        0 -> waypoint
        90 -> Waypoint(waypoint.y, -1 * waypoint.x)
        180 -> Waypoint(-1 * waypoint.x, -1 * waypoint.y)
        270 -> Waypoint(-1 * waypoint.y, waypoint.x)
        else -> error("unknown direction $direction")
    }

    fun updateWaypoint(waypoint: Waypoint, instruction: Instruction): Waypoint = when (instruction.code) {
        Code.N -> waypoint.copy( y = waypoint.y + instruction.value)
        Code.E -> waypoint.copy( x = waypoint.x + instruction.value)
        Code.S -> waypoint.copy( y = waypoint.y - instruction.value)
        Code.W -> waypoint.copy( x = waypoint.x - instruction.value)
        Code.L -> rotate(waypoint, (360 - instruction.value))
        Code.R -> rotate(waypoint, instruction.value)
        else -> error("not a waypoint instruction")
    }

    fun takeAction(boat: Boat, instruction: Instruction): Boat = when (instruction.code) {
        Code.F -> Boat(boat.x + boat.waypoint.x * instruction.value, boat.y + boat.waypoint.y * instruction.value, boat.waypoint)
        else -> Boat(boat.x, boat.y, updateWaypoint(boat.waypoint, instruction))
    }

    fun List<Instruction>.part2() = fold(Boat(0, 0, Waypoint(10, 1)), { acc, instruction -> takeAction(acc, instruction) })
        .let { boat -> abs(boat.x) + abs(boat.y) }
}

fun main(): Unit {
    Day12Part1.run {

        val sample = load("day12_data_sample.txt").toInstructions()
        val challenge = load("day12_data.txt").toInstructions()

        println(sample.part1()) // 25
        println(challenge.part1()) // 2270

    }

    Day12Part2.run {

        val sample = load("day12_data_sample.txt").toInstructions()
        val challenge = load("day12_data.txt").toInstructions()

        println(sample.part2()) // 286
        println(challenge.part2()) // 138669
    }
}