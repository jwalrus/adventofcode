package jwalrus.adventofcode

import jwalrus.adventofcode.util.load

object Day16 {

    data class Rule(val name: String, val left: IntRange, val right: IntRange) {
        fun toSet(): Set<Int> = (left.map { it }.toSet()).union(right.map { it }.toSet())
    }

    fun List<String>.parseRules(): List<Rule> {
        val regex = "([a-z ]+): (\\d+)-(\\d+) or (\\d+)-(\\d+)".toRegex()
        return map { s -> regex.find(s) }
            .map { mr -> mr!!.destructured }
            .map { (s, a, b, c, d) -> Rule(s.trim(), a.toInt()..b.toInt(), c.toInt()..d.toInt()) }
    }

    private fun String.parseInts(): List<Int> = split(",").map { it.toInt() }
    fun List<String>.parseInts(): List<List<Int>> = map { it.parseInts() }

    fun part1(rules: List<Rule>, tickets: List<List<Int>>) = run {
        val valid = rules.flatMap { it.toSet() }.toSet()
        tickets.map { it.toSet() }.flatMap { it - valid }.sum()
    }

    fun part2(rules: List<Rule>, myTicket: List<Int>, others: List<List<Int>>) = run {
        val valid = rules.flatMap { it.toSet() }.toSet()
        val validTickets = others.filter { (it - valid).isEmpty() }

        val map = rules.map { it.name to mutableSetOf<Int>() }.toMap().toMutableMap()
        val n = myTicket.size

        for (ix in 0 until n) {
            val digits = validTickets.map { it[ix] }
            for (rule in rules) {
                if (digits.all { it in rule.left || it in rule.right }) {
                    map[rule.name]!!.add(ix)
                }
            }
        }

        while (map.values.any { it.size > 1}) {

            for ((key,v) in map) {
                if (v.size == 1) {
                    val ix = v.first()
                    map.filter { (k,_) -> k != key }.forEach { (_, v) -> v.remove(ix) }
                }
            }
        }

        val indices = map.filter { (k,_) -> k.startsWith("departure") }.map { (_,v) -> v.first() }
        indices.map { myTicket[it].toLong() }.reduce(Long::times)
    }
}

fun main() = Day16.run {

    val sampleRules = load("day16_rules_sample.txt").parseRules()
    val sampleTicket = load("day16_myticket_sample.txt").parseInts().first()
    val sampleNearby = load("day16_nearby_sample.txt").parseInts()

    val sampleRules2 = load("day16_rules_sample2.txt").parseRules()
    val sampleTicket2 = load("day16_myticket_sample2.txt").parseInts().first()
    val sampleNearby2 = load("day16_nearby_sample2.txt").parseInts()

    val challengeRules = load("day16_rules.txt").parseRules()
    val challengeTicket = load("day16_myticket.txt").parseInts().first()
    val challengeNearby = load("day16_nearby.txt").parseInts()

    println(part1(sampleRules, sampleNearby))
    println(part1(challengeRules, challengeNearby))

//    println(part2(sampleRules2, sampleTicket2, sampleNearby2))
    println(part2(challengeRules, challengeTicket, challengeNearby)) // 3029180675981

}