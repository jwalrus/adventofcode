package jwalrus.adventofcode

import arrow.core.ListK
import arrow.core.extensions.fx
import arrow.core.k
import jwalrus.adventofcode.Day01Monad.part1
import jwalrus.adventofcode.Day01Monad.part2
import jwalrus.adventofcode.util.load

/* **************************
 * Take 1: Using ListK Monad
 * **************************/
object Day01Monad {

    fun List<Int>.part1(target: Int): Int = this.k().run {
        ListK.fx {
            val x = !this@run
            val y = !this@run.filter { it != x && x + it == target }.k()
            x to y
        }.first().let { (x, y) -> x * y }
    }

    // stupid inefficient
    fun List<Int>.part2(target: Int): Int = this.k().run {
        ListK.fx {
            val x = !this@run
            val y = !this@run.filter { it != x }.k()
            val z = !this@run.filter { it != x && it != y && x + y + it == target }.k()
            Triple(x, y, z)
        }.first().let { (x, y, z) -> x * y * z }
    }
}

/* *************************************************
 * Take 2: More efficient kotlin-only implementation
 * *************************************************/
object Day01 {

    private fun List<Long>.go_(target: Long): Long? = asSequence()
        .firstOrNull { binarySearch(target - it) > -1 }
        ?.let { it * (target - it) }

    fun part1(xs: List<Long>, target: Long): Long? = xs.sorted().go_(target)

    fun List<Long>.part2(target: Long): Long? {
        tailrec fun go(x: Long, xs: List<Long>): Long? = when (val result = xs.go_(target - x)) {
            null -> go(xs[0], xs.drop(1))
            else -> x * result
        }

        return when (isNotEmpty()) {
            true -> sorted().let { go(it[0], it.drop(1)) }
            false -> null
        }
    }
}

fun main() {

    Day01Monad.run {

        val sample = listOf(1721, 979, 366, 299, 675, 1456)
        val challenge = load("day01_data.txt").map(String::toInt)

        println(sample.part1(2020)) // 514_579
        println(challenge.part1(2020)) // 928_896
        println(sample.part2(2020)) // 241_861_950
        println(challenge.part2(2020)) // 295_668_576
    }

    Day01.run {

        val sample = listOf(1721L, 979L, 366L, 299L, 675L, 1456L)
        val challenge = load("day01_data.txt").map(String::toLong)

        println(part1(sample, 2020)) // 514_579
        println(part1(challenge, 2020)) // 928_896
        println(sample.part2(2020)) // 241_861_950
        println(challenge.part2(2020)) // 295_668_576
    }
}

