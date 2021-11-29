package jwalrus.adventofcode

import jwalrus.adventofcode.util.load
import java.math.BigInteger

object Day10 {

    fun List<Int>.part1(): Int {
        tailrec fun go(xs: List<Int>, prev: Int, acc: MutableMap<Int, Int>): Int =
            if (xs.isEmpty())
                acc[1]!! * acc[3]!!
            else {
                acc[xs[0] - prev] = acc[xs[0] - prev]!! + 1
                go(xs.drop(1), xs[0], acc)
            }
        return go(sorted(), 0, mutableMapOf(1 to 0, 2 to 0, 3 to 1))
    }


    fun List<Int>.part2(): BigInteger {
        tailrec fun go(xs: List<Int>, cache: MutableMap<Int, BigInteger>): BigInteger {
            return if (xs.isEmpty()) cache[cache.keys.maxOrNull()!!]!!
            else {
                val i = xs.first()
                cache[i] = listOf(1, 2, 3).map { cache[i - it] ?: BigInteger.ZERO }.reduce(BigInteger::plus)
                go(xs.drop(1), cache)
            }
        }
        return go(sorted(), mutableMapOf(0 to BigInteger.ONE))
    }
}

fun main() = Day10.run {

    val sample = load("day10_data_sample.txt").map(String::toInt)
    val challenge = load("day10_data.txt").map(String::toInt)

    println(sample.part1()) // 220
    println(challenge.part1()) // 2080

    println(sample.part2()) // 19208
    println(challenge.part2()) // 6908379398144
}