package jwalrus.adventofcode

import jwalrus.adventofcode.util.load

object Day07 {

    private fun String.clean() = replace("bags", "").replace("bag", "").trim()

    private fun splitLine(s: String) = s.split(" contain ").let { it[0].clean() to it[1] }

    private fun splitList(s: String) =
        if (s.contains("no other bags"))
            emptyMap()
        else s.replace(".", "").split(", ").map { str ->
            str.dropWhile { it.isDigit() }.clean() to str.takeWhile { it.isDigit() }.toInt()
        }.toMap()

    fun List<String>.parseToMap(): Map<String, Map<String, Int>> =
        map(Day07::splitLine).map { (k, v) -> k to splitList(v) }.toMap()

    fun Map<String, Map<String, Int>>.invert(): Map<String, Set<String>> {
        return map { (k, _) -> k to filterValues { it.containsKey(k) }.keys }.toMap()
    }

    fun Map<String, Set<String>>.part1(bag: String): Set<String> = getOrDefault(bag, emptySet()).let { set ->
        set.union(if (set.isEmpty()) set else set.map { part1(it) }.reduce(Set<String>::union))
    }


    fun Map<String, Map<String, Int>>.part2(bag: String): Int = getOrDefault(bag, emptyMap()).let {
        if (it.isEmpty()) 0 else it.map { (k, v) -> v * (1 + part2(k)) }.sum()
    }
}

fun main(): Unit = Day07.run {
    val sample = load("day07_data_sample.txt")
    val challenge = load("day07_data.txt")

    println(sample.parseToMap().invert().part1("shiny gold").size)    //    4
    println(challenge.parseToMap().invert().part1("shiny gold").size) //  254
    println(sample.parseToMap().part2("shiny gold"))         //   32
    println(challenge.parseToMap().part2("shiny gold"))      // 6006
}