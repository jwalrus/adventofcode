package jwalrus.adventofcode


import jwalrus.adventofcode.util.load

object Day19 {

    sealed class Rule {
        data class Branch(val values: List<List<Int>>) : Rule()
        data class Leaf(val value: String) : Rule()
    }

    private fun parseBranch(s: String): Pair<Int, Rule> {
        val key = s.takeWhile { it != ':' }.toInt()
        val value = s.dropWhile { it != ':' }.drop(1).split("|")
            .map { it.trim().split(" ").map { i -> i.toInt() } }
        return key to Rule.Branch(value)
    }

    private fun parseLeaf(s: String): Pair<Int, Rule> =
        s.split(": ").let { it[0].toInt() to Rule.Leaf(it[1].replace("\"", "")) }

    private fun parseRule(s: String): Pair<Int, Rule> = if (s.contains("[a-zA-Z]".toRegex())) parseLeaf(s) else parseBranch(s)

    fun List<String>.parseRules(): Map<Int, Rule> = map(Day19::parseRule).toMap()

    /**
     * Again, assist goes to kotlin slack's #advent-of-code channel
     */
    fun valid(s: String, rules: Map<Int, Rule>, stack: List<Int> = mutableListOf(0)): Boolean {
        return when {
            s.isEmpty() -> stack.isEmpty()
            stack.isEmpty() -> s.isEmpty()
            else -> when (val rule = rules[stack.first()]!!) {
                is Rule.Leaf -> if ("${s.first()}" == rule.value) valid(s.drop(1), rules, stack.drop(1)) else false
                is Rule.Branch -> rule.values.any { valid(s, rules, it + stack.drop(1)) }
            }
        }
    }
}

fun main() = Day19.run {

    val sampleRules = load("day19_data_rules_sample.txt").parseRules().also(::println)
    val sampleMsgs = load("day19_data_messages_sample.txt")
    val challengeRules = load("day19_data_rules.txt").parseRules().toMutableMap()
    val challengeMsgs = load("day19_data_messages.txt")

    println(sampleMsgs.count { msg -> valid(msg, sampleRules, listOf(0)) }) // 2
    println(challengeMsgs.count { msg -> valid(msg, challengeRules, listOf(0))}) // 235

    challengeRules[8] = Day19.Rule.Branch(listOf(listOf(42), listOf(42, 8)))
    challengeRules[11] = Day19.Rule.Branch(listOf(listOf(42, 31), listOf(42, 11, 31)))

    println(challengeMsgs.count { msg -> valid(msg, challengeRules, listOf(0))}) // 379
}