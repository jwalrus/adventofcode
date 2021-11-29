package jwalrus.adventofcode.util

import io.kotest.core.spec.style.DescribeSpec
import io.kotest.data.forAll
import io.kotest.data.row
import io.kotest.matchers.collections.shouldContainInOrder

class SequenceUtilSpec : DescribeSpec({

    describe("createVector") {

        forAll(
            row(0 to 0, 1 to 1, listOf(0 to 0, 1 to 1, 2 to 2, 3 to 3)),
            row(0 to 0, 1 to -1, listOf(0 to 0, 1 to -1, 2 to -2, 3 to -3)),
            row( 2 to 1, 0 to -1, listOf(2 to 1, 2 to 0, 2 to -1, 2 to -2)),
            row(1 to 3, -1 to -3, listOf(1 to 3, 0 to 0, -1 to -3, -2 to -6))
        ) { start, direction, expectation ->
            createVector(start, direction).take(4).toList() shouldContainInOrder expectation
        }
    }
})
