package jwalrus.adventofcode

import jwalrus.adventofcode.util.load

object Day18 {

    fun eval(left: Long, op: String, right: String): Long = when (op) {
        "+" -> left + right.toLong()
        "*" -> left * right.toLong()
        else -> error("unsupported operation $op")
    }

    private fun eval(s: String): Long {

        tailrec fun go(cs: List<String>, acc: Long): Long =
            if (cs.isEmpty()) acc
            else go(cs.drop(2), eval(acc, cs[0], cs[1]))

        val cs = s.split(" ").filterNot { it.isBlank() }
        return go(cs.drop(1), cs.first().toLong())
    }

    val addRegex = "([0-9\\+ ]+)".toRegex()

    fun weirdEval(s: String): String = addRegex.replace(s) { " ${eval(it.value.trim() )} " }


    val regex = "(\\([0-9\\+\\* ]+\\))".toRegex()

    fun evalParen(s: String): String {
        return regex.replace(s) {
            "${eval(weirdEval(it.value.replace("(", "").replace(")", "").trim()))}"
        }
    }

    fun evaluate(expression: String): Long {
        var s = expression
        while (s.contains("(") || s.contains(")")) {
            s = evalParen(s)
        }

        while(s.contains("+")) {
            s = weirdEval(s)
        }
        return eval(s)
    }

    fun List<String>.part1() = map { evaluate(it) }.reduce(Long::plus)
    fun List<String>.part2() = map { evaluate(it) }.reduce(Long::plus)
}

fun main(): Unit = Day18.run {

    val sample = load("day18_data_sample.txt")
    val challenge = load("day18_data.txt")

    /**
     * to run part 1, checkout the corresponding commit
     */
//    println(eval(3, "+", "1"))
//    println(eval(3, "*", "2"))
//    println(evaluate("1 + 2 * 3 + 4 * 5 + 6")) // 71
//    println(evalParen("1 + (2 * 3) + (4 * (5 + 6))")) // 51
//    println(evaluate("1 + (2 * 3) + (4 * (5 + 6))")) // 51
//    println(evaluate("2 * 3 + (4 * 5)")) // 26
//    println(evaluate("5 + (8 * 3 + 9 + 3 * 4 * 3)")) // 437
//    println(evaluate("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")) // 12240
//    println(evaluate("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")) // 13632
//
//    println(challenge.part1()) // 280014646144

    println(evaluate("1 + 2 * 3 + 4 * 5 + 6")) // 231
    println(evaluate("1 + (2 * 3) + (4 * (5 + 6))")) // 51
    println(evaluate("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")) // 23340

    println(challenge.part2()) // 9966990988262

}