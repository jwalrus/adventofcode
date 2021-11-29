package jwalrus.adventofcode

import jwalrus.adventofcode.util.load

object Day09 {

    fun <T> subSequences(ts: List<T>, len: Int): Sequence<List<T>> = sequence {
        var src = ts
        while (src.count() >= len) {
            yield(src.take(len))
            src = src.drop(1)
        }
    }

    fun List<Long>.part1(pre: Int) = subSequences(this, pre + 1)
        .map { xs -> xs.dropLast(1) to xs.last() }
        .filter { (xs, target) -> Day01.part1(xs, target) == null }
        .first().second

    fun List<Long>.part2(target: Long): Long {
        tailrec fun go(xs: List<Long>): Pair<Long, Int> {
            val sums = xs.runningReduce(Long::plus)
            return if (sums.contains(target))
                sums.takeWhile { it <= target }.let { it.first() to it.size }
            else
                go(xs.drop(1))
        }

        val (start, count) = go(this)
        return dropWhile { it != start }.take(count)
            .let { it.maxOrNull()!! + it.minOrNull()!! }
    }

}

fun main() = Day09.run {
    val sample = load("day09_data_sample.txt").map(String::toLong)
    val challenge = load("day09_data.txt").map(String::toLong)

    println(sample.part1(5)) // 127
    println(challenge.part1(25)) // 26796446

    println(sample.part2(sample.part1(5))) // 62
    println(challenge.part2(challenge.part1(25))) // 3353494
}
