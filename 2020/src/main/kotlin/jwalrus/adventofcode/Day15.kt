package jwalrus.adventofcode

object Day15 {

    private fun List<Int>.memory(): Sequence<Int> = sequence {
        val history = mutableMapOf<Int, Int>()
        subList(0, size - 1).mapIndexed { ix, l -> l to ix }.toMap(history)
        var speak = last()

        yieldAll(subList(0, size - 1))
        var ix = size - 1
        while (true) {
            yield(speak)
            speak = ix - (history.put(speak, ix) ?: ix)
            ix += 1
        }
    }

    fun List<Int>.part1() = memory().take(2020).last()
    fun List<Int>.part2() = memory().take(30000000).last()
}

fun main() = Day15.run {

    val sample = listOf(0,3,6)
    val sample1 = listOf(1,3,2)
    val sample2 = listOf(2,1,3)
    val sample3 = listOf(1,2,3)
    val challenge = listOf(20,9,11,0,1,2)

    println(sample.part1()) // 436
    println(sample1.part1()) // 1
    println(sample2.part1()) // 10
    println(sample3.part1()) // 27
    println(challenge.part1()) // 1111
    println(sample.part2()) // 175594
    println(challenge.part2()) // 48568
}