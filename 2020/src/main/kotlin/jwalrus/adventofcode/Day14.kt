package jwalrus.adventofcode

import jwalrus.adventofcode.util.load

object Day14 {

    fun getMask(s: String) = s.split("=")[1].trim()
    fun getMemAddr(s: String) = "mem\\[(\\d+)\\] = (\\d+)".toRegex().find(s)!!.destructured.let { (l,r) -> l.toLong() to r.toLong() }
    fun Long.toBin36(): String = this.toString(2).padStart(36, '0')
    fun applyMask(mask: String, num: String): String = mask.zip(num).map { (m, c) -> if (m == 'X') c else m }.joinToString("")
    fun binToLong(b: String) = b.toLong(2)

    fun decodeV2(mask: String, num: String): List<String> {
        val raw = mask.zip(num)
            .map { (m, c) -> if (m == '0') c else m }
            .joinToString("")

        var addrs = mutableListOf<String>()
        addrs.add("$raw")

        for (i in raw.indices) {

            if (raw[i] == 'X') {

                val newAddrs = mutableListOf<String>()

                for (addr in addrs) {
                    val zero = addr.toCharArray()
                    val one = addr.toCharArray()

                    zero[i] = '0'
                    one[i] = '1'

                    newAddrs.add(zero.joinToString(""))
                    newAddrs.add(one.joinToString(""))
                }
                addrs = newAddrs
            }
        }

        return addrs.also(::println)
    }

    fun List<String>.part1() = run {

        val memMap = mutableMapOf<Long, Long>()
        var mask = ""
        for (s in this) {
            if (s.startsWith("mask")) {
                mask = getMask(s)
            } else {
                val (addr, num) = getMemAddr(s)
                memMap[addr] = binToLong( applyMask(mask, num.toBin36()) )
            }
        }
        memMap.values.sum()
    }

    fun List<String>.part2() = run {

        val memMap = mutableMapOf<Long, Long>()
        var mask = ""
        for (s in this) {
            if (s.startsWith("mask")) {
                mask = getMask(s)
            } else {
                val (addr, num) = getMemAddr(s)

                for (a in decodeV2(mask, addr.toBin36())) {
                    memMap[binToLong(a)] = num
                }
            }
        }
        memMap.values.sum()
    }
}

fun main() = Day14.run {

    val sample = load("day14_data_sample.txt")
    val sample2 = load("day14_data_sample2.txt")
    val challenge = load("day14_data.txt")

    println(sample.part1()) // 165
    println(challenge.part1()) // 13865835758282
    println(sample2.part2()) // 208
    println(challenge.part2()) // 4195339838136
}