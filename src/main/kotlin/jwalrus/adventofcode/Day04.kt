package jwalrus.adventofcode

import arrow.core.*
import arrow.core.extensions.either.applicative.applicative
import jwalrus.adventofcode.DayO4.part1
import jwalrus.adventofcode.DayO4.part2
import jwalrus.adventofcode.util.load

private typealias Option<A> = Either<Unit, A>

data class Height(
    val value: Int,
    val unit: String
)

data class Passport(
    val byr: Int,
    val iyr: Int,
    val eyr: Int,
    val hgt: Height,
    val hcl: String,
    val ecl: String,
    val pid: String,
    val cid: String?
)

fun mkHeight(s: String?): Option<Height> = s?.let {
    "^(\\d+)(cm|in)$".toRegex().matchEntire(s)?.groupValues?.let { (_, measure, unit) ->
        when (unit) {
            "cm" -> between(measure, 150..193)
            "in" -> between(measure, 59..76)
            else -> Unit.left()
        }.map { value -> Height(value, unit) }
    }
} ?: Unit.left()


private fun splitKeyValue(s: String): Pair<String, String> = s.trim().split(':').let { it[0] to it[1] }
private fun String.parseToMap() = split(" ").map(::splitKeyValue).toMap()

private fun between(s: String?, range: IntRange) = s?.toIntOrNull()
    ?.let { if (it in range) it.right() else Unit.left() }
    ?: Unit.left()

private fun matches(s: String?, regex: Regex) = if (s?.matches(regex) == true) s.right() else Unit.left()

fun byr(s: String?): Option<Int> = between(s, 1920..2002)
fun iyr(s: String?): Option<Int> = between(s, 2010..2020)
fun eyr(s: String?): Option<Int> = between(s, 2020..2030)
fun hgt(s: String?): Option<Height> = mkHeight(s)
fun hcl(s: String?): Option<String> = matches(s, "#[0-9a-f]{6}".toRegex())
fun ecl(s: String?): Option<String> = matches(s, "(amb|blu|brn|gry|grn|hzl|oth)".toRegex())
fun pid(s: String?): Option<String> = matches(s, "(\\d{9})".toRegex())
fun cid(s: String?): Option<String> = s?.right() ?: "".right()

fun mkPassport(s: String): Option<Passport> = s.parseToMap().let {
    Either.applicative<Unit>().tupledN(
        byr(it["byr"]),
        iyr(it["iyr"]),
        eyr(it["eyr"]),
        hgt(it["hgt"]),
        hcl(it["hcl"]),
        ecl(it["ecl"]),
        pid(it["pid"]),
        cid(it["cid"])
    ).fix().map { (byr, iyr, eyr, hgh, hcl, ecl, pid, cid) ->
        Passport(byr, iyr, eyr, hgh, hcl, ecl, pid, cid)
    }
}


private fun List<String>.extractPassports(): List<String> {
    tailrec fun go(xs: List<String>, acc: MutableList<String>): List<String> {
        return if (xs.isEmpty()) acc
        else {
            acc.add(xs.takeWhile { it.isNotBlank() }.joinToString(" "))
            go(xs.dropWhile { it.isNotBlank() }.dropWhile { it.isBlank() }, acc)
        }
    }

    return go(this, mutableListOf())
}

object DayO4 {

    fun List<String>.part1(): Int = extractPassports()
        .map { it.parseToMap() }
        .filter { if (it.containsKey("cid")) it.count() == 8 else it.count() >= 7 }
        .count()


    fun List<String>.part2(): Int = extractPassports()
        .map { mkPassport(it) }
        .filter { it.isRight() }
        .count()
}

fun main(): Unit = DayO4.run {
    val sample = load("day04_data_sample.txt")
    val validSample = load("day04_data_sample_valid.txt")
    val challenge = load("day04_data.txt")

    println(sample.part1()) // 2
    println(challenge.part1()) // 228
    println(validSample.part2()) // 4
    println(challenge.part2()) // 175
}
