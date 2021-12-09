defmodule Day06 do
  def input do
    File.read!("./test/day06.txt")
    |> String.trim()
    |> String.split(",")
    |> Enum.map(&String.to_integer/1)
  end

  def calculate(i, counts) do
    case i do
      6 -> Map.get(counts, 0, 0) + Map.get(counts, 7, 0)
      8 -> Map.get(counts, 0, 0)
      _ -> Map.get(counts, i + 1, 0)
    end
  end

  def advance(counts) do
    Enum.reduce(0..8, %{}, fn x, acc -> Map.put(acc, x, Day06.calculate(x, counts)) end)
  end

  def part1(xs, n \\ 80) do
    1..n
    |> Enum.reduce(Enum.frequencies(xs), fn _, acc -> Day06.advance(acc) end)
    |> then(&Map.values/1)
    |> Enum.sum()
  end

  def part2(xs) do
    part1(xs, 256)
  end
end

defmodule Day06Test do
  use ExUnit.Case

  test "loads instructions" do
    assert Day06.input() |> Enum.take(5) == [5, 1, 1, 1, 3]
  end

  test "calculates next stage" do
    counts = %{0 => 1, 7 => 1}
    assert Day06.calculate(6, counts) == 2
  end

  test "advances counts" do
    counts = %{0 => 1, 7 => 1}

    assert Day06.advance(counts) == %{
             0 => 0,
             1 => 0,
             2 => 0,
             3 => 0,
             4 => 0,
             5 => 0,
             6 => 2,
             7 => 0,
             8 => 1
           }
  end

  test "part1" do
    assert Day06.input() |> Day06.part1() == 380_243
  end

  test "part2" do
    assert Day06.input() |> Day06.part2() == 1_708_791_884_591
  end
end
