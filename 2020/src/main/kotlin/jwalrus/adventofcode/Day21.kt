package jwalrus.adventofcode

import jwalrus.adventofcode.util.load

object Day21 {

    private fun String.parseAllergens(): Set<String> = trim().replace(")", "").split(", ").toSet()
    private fun String.parseIngredients(): Set<String> = trim().split(" ").toSet()
    private fun String.parse(): Food = split(" (contains").let { Food(it[0].parseIngredients(), it[1].parseAllergens()) }
    fun List<String>.parse(): List<Food> = map { it.parse() }

    data class Food(val ingredients: Set<String>, val allergens: Set<String>)

    fun List<Food>.part1() = run {
        val allergens = flatMap { it.allergens }.toSet()
        val ingredients = flatMap { it.ingredients }.toSet()

        val set = mutableSetOf<Set<String>>()

        for (allergen in allergens) {
            val foods = filter { it.allergens.contains(allergen) }
            val intersection = foods.map { it.ingredients }.reduce(Set<String>::intersect)
            set.add(ingredients - intersection)
        }

        val notPoison = set.reduce(Set<String>::intersect)
        val num = flatMap { it.ingredients }.count { notPoison.contains(it) }

        num to notPoison
    }


    fun List<Food>.part2() = run {
        val poison = flatMap { it.ingredients }.toSet() - part1().second
        val allergens = flatMap { it.allergens }.toSet()
        val foods = map { Food(poison.intersect(it.ingredients), it.allergens) }

        var map = mutableMapOf<String, Set<String>>()

        for (allergen in allergens) {
            val common = foods.filter { it.allergens.contains(allergen) }
            val intersection = common.map { it.ingredients }.reduce(Set<String>::intersect)
            map[allergen] = intersection
        }

        val result = mutableListOf<Pair<String, String>>()

        while (map.isNotEmpty()) {
            val (a, ii) = map.toList().firstOrNull { it.second.size == 1 } ?: break
            result.add(a to ii.first())
            map.remove(a)
            map.forEach { (k,v) -> map[k] = v - ii }
        }

        result.sortedBy { it.first }.joinToString(",") { it.second }
    }
}

fun main() = Day21.run {
    val sample = load("day21_data_sample.txt").parse().also(::println)
    val challenge = load("day21_data.txt").parse()

    println(sample.part1().first) // 5
    println(challenge.part1().first) // 2779
    println(sample.part2()) // mxmxvkd,sqjhc,fvjkl
    println(challenge.part2()) // lkv,lfcppl,jhsrjlj,jrhvk,zkls,qjltjd,xslr,rfpbpn
}