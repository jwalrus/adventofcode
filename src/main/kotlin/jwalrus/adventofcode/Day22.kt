package jwalrus.adventofcode

import jwalrus.adventofcode.util.loadGroups

typealias Hand = List<Long>

object Day22 {

    private fun parseHand(ss: List<String>) = ss.drop(1).map(String::toLong)
    fun List<List<String>>.parse() = parseHand(this[0]) to parseHand(this[1])

    private fun List<Long>.plus(a: Long, b: Long) = plus(listOf(a, b))
    fun Hand.score() = reversed().mapIndexed { i, l -> (i + 1) * l }.reduce(Long::plus)

    private tailrec fun combat(h1: Hand, h2: Hand): Hand = when {
        h1.isEmpty() -> h2
        h2.isEmpty() -> h1
        else -> {
            val c1 = h1.first()
            val c2 = h2.first()
            if (c1 > c2)
                combat(h1.drop(1).plus(c1, c2), h2.drop(1))
            else
                combat(h1.drop(1), h2.drop(1).plus(c2, c1))
        }
    }


    fun Pair<Hand, Hand>.part1(): Hand = combat(first, second)

    private tailrec fun rcombat(h1: Hand, h2: Hand, previous: Set<Pair<Hand, Hand>> = emptySet()): Pair<Boolean, Hand> {

        if ((h1 to h2) in previous) return  true to h1
        val prev = previous.plus(h1 to h2)

        return when {
            h1.isEmpty() -> false to h2
            h2.isEmpty() -> true to h1
            else -> {
                val c1 = h1.first()
                val c2 = h2.first()
                val hh1 = h1.drop(1)
                val hh2 = h2.drop(1)


                if (h1.size > c1 && h2.size > c2) {
                    val (winner, _) = rcombat(hh1.take(c1.toInt()), hh2.take(c2.toInt()))
                    if (winner) {
                        rcombat(hh1.plus(c1, c2), hh2, prev)
                    } else {
                        rcombat(hh1, hh2.plus(c2, c1), prev)
                    }
                } else {
                    if (c1 > c2) {
                        rcombat(hh1.plus(c1, c2), hh2, prev)
                    } else {
                        rcombat(hh1, hh2.plus(c2, c1), prev)
                    }
                }
            }
        }
    }

    fun Pair<Hand, Hand>.part2(): Hand = rcombat(first, second).second
}

fun main() = Day22.run {
    val sample = loadGroups("day22_data_sample.txt").parse()
    val challenge = loadGroups("day22_data.txt").parse()

    // part1
    println(sample.part1().score()) // 306
    println(challenge.part1().score()) // 32472

    println(sample.part2())
    println(sample.part2().score()) // 291
//    println(challenge.part2().size)
    println(challenge.part2().score()) // ???
//    println(challenge.part2().score()) // != 34838 (too low)
}