package jwalrus.adventofcode.util

import arrow.core.*
import arrow.core.extensions.either.applicative.applicative
import arrow.core.extensions.list.traverse.traverse
import java.nio.file.Paths

fun load(name: String): List<String>
        = Paths.get("src", "main", "resources", name).toFile().readLines()

fun loadText(name: String): String
        = Paths.get("src", "main", "resources", name).toFile().readText()

fun loadGroups(name: String): List<List<String>>
        = loadText(name).split("\n\n").map { it.trim().split("\n") }

/**
 * Use [traverse] from Arrow under the hood. Example usage:
 * ```
 *
 * load("day01_data.txt") { s ->
 *      s.toIntOrNull()?.right() ?: "$s cannot be parsed to int!".left()
 * } // Right(ListK(123, 456, 8574, ...))
 */
fun <T> load(name: String, f: (String) -> Either<String, T>): Either<String, ListK<T>> {
    return load(name).k().traverse(Either.applicative()) { f(it) }.fix()
}