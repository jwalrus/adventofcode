package jwalrus.adventofcode

import jwalrus.adventofcode.util.load

object Day08 {

    enum class Op { NOP, ACC, JMP }

    private fun String.parseInt(): Int = if (startsWith('+')) drop(1).toInt() else drop(1).toInt() * -1
    private fun String.parseOp(): Op = Op.valueOf(this.toUpperCase())
    private fun String.parse(): Pair<Op, Int> = split(" ").let { it[0].parseOp() to it[1].parseInt() }
    fun List<String>.parse(): List<Pair<Op, Int>> = map { it.parse() }


    fun List<Pair<Op, Int>>.part1(): Pair<Boolean, Int> {

        tailrec fun go(ix: Int, visited: MutableSet<Int>, acc: Int): Pair<Boolean, Int> {
            return when {
                ix >= size -> Pair(true, acc)
                ix in visited -> Pair(false, acc)
                else -> {
                    val (op, x) = get(ix)
                    visited.add(ix)
                    when (op) {
                        Op.NOP -> go(ix + 1, visited, acc)
                        Op.ACC -> go(ix + 1, visited, acc + x)
                        Op.JMP -> go(ix + x, visited, acc)
                    }
                }
            }
        }

        return go(0, mutableSetOf(), 0)
    }

    private fun switch(op: Op) = when (op) {
        Op.ACC -> Op.ACC
        Op.JMP -> Op.NOP
        Op.NOP -> Op.JMP
    }

    fun List<Pair<Op, Int>>.part2(): Int = asSequence() // lazy eval
            .mapIndexed { i, (op, x) -> i to Pair(switch(op), x) }
            .filter { (_,v) -> v.first != Op.ACC }
            .map { (i, p) -> this.toMutableList().apply { set(i, p) } }
            .map { it.part1() }
            .first { it.first }.second
}

fun main() = Day08.run {
    val sample = load("day08_data_sample.txt").parse()
    val challenge = load("day08_data.txt").parse()

    println(sample.part1().second) // 5
    println(challenge.part1().second) // 1337

    println(sample.part2()) // 8
    println(challenge.part2()) // 1358
}