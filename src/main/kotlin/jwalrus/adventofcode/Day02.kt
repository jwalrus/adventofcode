package jwalrus.adventofcode

import jwalrus.adventofcode.util.load

object Day02 {

    private data class Row(val a: Int, val b: Int, val c: Char, val d: String)

    private val regex: Regex = "^(\\d+)-(\\d+) ([A-Za-z]): (.+)$".toRegex()

    private fun String.toRow(): Row = regex.find(this)!!.destructured
        .let { (a, b, c, d) -> Row(a.toInt(), b.toInt(), c.toCharArray()[0], d) }

    private fun String.containsCharBetween(c: Char, lower: Int, upper: Int): Boolean = count { it == c } in lower..upper

    private fun String.containsCharAtIndexExactlyOnce(c: Char, ix: Set<Int>): Boolean =
        filterIndexed { index, char -> (index + 1) in ix && char == c }.length == 1

    fun List<String>.part1(): Int = asSequence().map { it.toRow() }
        .filter { tup -> tup.d.containsCharBetween(tup.c, tup.a, tup.b) }
        .count()

    fun List<String>.part2(): Int = asSequence().map { it.toRow() }
        .filter { tup -> tup.d.containsCharAtIndexExactlyOnce(tup.c, setOf(tup.a, tup.b)) }
        .count()
}

fun main() = Day02.run {
    val sample = listOf("1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc")
    val challenge = load("day02_data.txt")

    println(sample.part1()) // 2
    println(challenge.part1()) // 500

    println(sample.part2()) // 1
    println(challenge.part2()) // 313
}
