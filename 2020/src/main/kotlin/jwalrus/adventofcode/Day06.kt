package jwalrus.adventofcode

import jwalrus.adventofcode.util.loadGroups

object Day06 {

    private fun commonAnswers(xs: List<String>): Set<Char> = xs.map(CharSequence::toSet).reduce(Set<Char>::intersect)

    private fun uniqueAnswers(xs: List<String>): Set<Char> = xs.map(CharSequence::toSet).reduce(Set<Char>::union)

    fun List<List<String>>.part1() = map(Day06::uniqueAnswers).map(Set<Char>::size).sum()

    fun List<List<String>>.part2() = map(Day06::commonAnswers).map(Set<Char>::size).sum()
}

fun main(): Unit = Day06.run {

    val sample = loadGroups("day06_data_sample.txt")
    val challenge = loadGroups("day06_data.txt")

    println(sample.part1()) // 11
    println(challenge.part1()) // 6534
    println(sample.part2()) // 6
    println(challenge.part2()) // 3402
}