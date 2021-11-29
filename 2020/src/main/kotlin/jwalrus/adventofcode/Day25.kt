package jwalrus.adventofcode

object Day25 {

    private fun transformations(sn: Long): Sequence<Pair<Int, Long>>
        = generateSequence(0 to 1L) { (i, r) -> (i+1) to (r * sn) % 20201227L }.drop(1)
    private fun transform(sn: Long, ls: Int): Long = transformations(sn).take(ls).last().second
    private fun findLs(pub: Long): Int = transformations(7).dropWhile { it.second != pub }.first().first

    fun lastDay(pk1: Long, pk2: Long) = transform(pk1, findLs(pk2))
}

fun main() = Day25.run {
    println(lastDay(5764801L, 17807724L)) // 14897079
    println(lastDay(3469259L, 13170438L)) // 7269858
}