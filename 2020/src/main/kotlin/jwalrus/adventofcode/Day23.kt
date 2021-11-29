package jwalrus.adventofcode


object Day23 {

    private fun Map<Int, Int>.backToList(): List<Int> {
        val result = mutableListOf<Int>()
        var ix = 1
        for (i in 1..size) {
            ix = this[ix]!!
            result.add(ix)
        }
        return result
    }

    private fun move(map: MutableMap<Int, Int>, ic: Int): Int {
        val n1 = map[ic]!!
        val n2 = map[n1]!!
        val n3 = map[n2]!!
        val n4 = map[n3]!!

        var id = ic
        do {
            id = if (id > 1) id - 1 else map.size
        } while (id == n1 || id == n2 || id == n3)

        val idn = map[id]!!
        map[ic] = n4
        map[id] = n1
        map[n1] = n2
        map[n2] = n3
        map[n3] = idn

        return n4
    }

    fun List<Int>.part1(n: Int) = run {
        val map = mapIndexed { i,x -> x to get((i + 1) % size) }.toMap().toMutableMap()
        var cur = get(0)
        for (i in 1..n) cur = move(map, cur)
        map.backToList().dropLast(1).joinToString("")
    }

    fun List<Int>.part2(n: Int = 10_000_000) = run {
        val map = mutableMapOf<Int, Int>()
        mapIndexed { i, x ->  x to getOrElse(i + 1) { 10 } }.toMap(map)
        (10..1_000_000).map { it to it + 1 }.toMap(map)
        map[1_000_000] = get(0) // complete circle
        var cur = get(0)
        for (i in 1..n) cur = move(map, cur)

        val x = map[1]!!
        val y = map[x]!!
        x.toLong() * y.toLong()
    }

}

fun main() = Day23.run {
    val sample = "389125467".map {"$it".toInt()}
    val challenge = "598162734".map {"$it".toInt()}

    println(sample.part1(10)) //92658374
    println(sample.part1(100)) //67384529
    println(challenge.part1(100)) //32658947

    println(sample.part2()) // 149245887792
    println(challenge.part2()) // 683486010900
}