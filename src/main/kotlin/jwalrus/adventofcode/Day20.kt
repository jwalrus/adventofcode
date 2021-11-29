package jwalrus.adventofcode

import jwalrus.adventofcode.util.loadGroups

object Day20 {

    private fun parseImage(ls: List<String>): Image {
        val id = ls.first().dropLast(1).takeLastWhile { it.isDigit() }.toInt()
        return Image(id, ls.drop(1))
    }
    fun List<List<String>>.parseImages() = map(Day20::parseImage)

    data class Image(val id: Int, val data: List<String>) {

        val top = data.first()
        val bottom = data.last()
        val left = data.map { it.first() }.joinToString("")
        val right = data.map { it.last() }.joinToString("")
        val edges: List<String> = listOf(
            top, right, bottom, left,
            top.reversed(), right.reversed(), bottom.reversed(), left.reversed()
        )

        val edgesWithId: List<Pair<Image, String>> = edges.map { this to it }

        fun neighbor(edge: String, map: Map<String, List<Image>>): Image? {
            return map[edge]?.firstOrNull { it.id != id }
        }

        fun neighborOnRight(map: Map<String, List<Image>>): Image? {
            return neighbor(right, map)?.let { n ->
                n.permutations().first { x ->
                    x.left == this.right
                }
            }
        }

        fun neighborOnBottom(map: Map<String, List<Image>>): Image? {
            return neighbor(bottom, map)?.let { n ->
                n.permutations().first { it.top == bottom }
            }
        }

        fun stripEdges(): List<String> {
            return data.drop(1).dropLast(1).map { it.drop(1).dropLast(1) }
        }

        fun rotate(): Image {
            val ii = data.size
            val jj = data.first().length
            val result = mutableListOf<String>()
            for (i in 0 until ii) {
                var line = ""
                for (j in 0 until jj) {
                    line += data[ii-1-j][i]
                }
                result.add(line)
            }
            return Image(id, result)
        }

        fun flip(): Image {
            val result = data.map { it.reversed() }
            return Image(id, result)
        }

        fun permutations(): List<Image> {
            val result = mutableListOf<Image>()
            var cur = this
            for (i in 1..4) {
               result.add(cur)
               result.add(cur.flip())
               cur = cur.rotate()
            }
            return result
        }
    }

    fun List<Image>.matches(): Map<String, List<Image>> = flatMap { it.edgesWithId }.groupBy({it.second}, {it.first})
    fun List<Image>.matchCounts(): Map<Image, Int> {
        val matches = matches().filter { it.value.size >= 2 }
        return map { img -> img to matches.values.count { ids -> ids.contains(img) }}.toMap()
    }

    fun List<Image>.assemble() = run {
        val matches = matches()
        val counts = matchCounts()

        val corners = counts.filter { it.value/2 == 2 }.keys
        val topLeft = corners.flatMap { it.permutations() }.first { it.neighbor(it.right, matches) != null && it.neighbor(it.bottom, matches) != null }

        val result = mutableListOf<MutableList<Image>>()
        var lhs: Image? = topLeft


        while (lhs != null) {

            val row = mutableListOf<Image>()
            row.add(lhs)

            var rhs: Image? = lhs.neighborOnRight(matches)

            while (rhs != null) {
                row.add(rhs)
                rhs = rhs.neighborOnRight(matches)
            }

            result.add(row)
            lhs = lhs.neighborOnBottom(matches)
        }

        result
    }

    fun List<Image>.format(): List<String> {
        return map { it.stripEdges() }
            .flatMap { img -> img.mapIndexed { index, s -> index to s }}
            .groupBy({it.first},{it.second})
            .values.map { it.joinToString("") }
    }

    fun List<List<Image>>.formatAll(): List<String> {
        return flatMap { it.format() }.toList()
    }

    fun String.dragons(dragon: Regex): Int {

        tailrec fun go(s: String, acc: Int): Int {
            return if (s.isEmpty()) acc
            else if (dragon.matches(s)) go(s.drop(1), acc + 1) else go(s.drop(1), acc)
        }
        return go(this, 0)
    }

    fun List<List<Image>>.bigImage(): Image = Image(-1, formatAll())

    fun List<Image>.part1() = matchCounts().filter { it.value == 4 }.keys.map { it.id.toLong() }.reduce(Long::times)
    fun List<Image>.part2() = run { 2 }
}

fun main() = Day20.run {
    val sample = loadGroups("day20_data_sample.txt").parseImages()
    val challenge = loadGroups("day20_data.txt").parseImages().also { println(it.size) }

    println(sample.matches())
    println(sample.matchCounts())

    println(sample.part1()) // 20899048083289
    println(challenge.part1()) // 8425574315321

//    sample.first().permutations().forEach(::println)
//
////    println(sample.part2()) // ???
////    println(challenge.part2()) // ???
//    sample.assemble().reversed().map { it.map { k -> k.id }}.forEach(::println)
//    sample.assemble().formatAll().reversed().forEach(::println)

//    challenge.assemble().formatAll().forEach(::println)

    val dragon = """..................#.{5}#....##....##....###.{4}.#..#..#..#..#..#.{7}"""
//    val dragon = """..................#((?=.*n).{6})#....##....##....###((?=.*n).{5}).#..#..#..#..#..#"""
    val dragonSample = sample.assemble().bigImage().permutations().map {
        val s = it.data.joinToString("")
        val c = dragon.toRegex().findAll(s).count()
        s to c
    }.first { it.second > 0 }

    println(dragonSample.let { (s, c) ->
        s.count { it == '#' } - c * dragon.count { it == '#' }
    })

    val dragon2 = """#.{77}#....##....##....###.{76}.#..#..#..#..#..#"""
//    val dragon2 = """..................#((?=.*n).{78})#....##....##....###((?=.*n).{77}).#..#..#..#..#..#"""
    val dragonChallenge = challenge.assemble().bigImage().permutations().map {
        val s = it.data.joinToString("")
        val c = dragon2.toRegex().findAll(s).count()
        s to c
    }.first { it.second > 0 }.also { println(it.second) }

    // THIS IS MAGIC SAUCE FOR PUZZLE
    val dragon3 = """^#.{77}#....##....##....###.{76}.#..#..#..#..#..#.+""".toRegex()
    println(dragonChallenge.first.dragons(dragon3)) // 24

    println(dragonChallenge.let { (s, c) ->
        s.count { it == '#' } - 24 * dragon.count { it == '#' }
    })
}