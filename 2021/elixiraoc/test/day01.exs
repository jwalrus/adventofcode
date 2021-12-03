defmodule Day01 do
  def data do
    File.stream!("./test/day01.txt")
    |> Stream.map(&String.trim/1)
    |> Stream.map(&String.to_integer/1)
  end

  def part1(xs, n \\ 1) do
    xs
    |> Stream.chunk_every(n, 1, :discard)
    |> Stream.chunk_every(2, 1, :discard)
    |> Enum.count(fn [x, y] -> Enum.sum(y) > Enum.sum(x) end)
  end

  def part2(xs) do
    part1(xs, 3)
  end
end

defmodule Day01Test do
  use ExUnit.Case
  doctest Elixiraoc

  test "part1" do
    assert Day01.data() |> Day01.part1() == 1482
  end

  test "part2" do
    assert Day01.data() |> Day01.part2() == 1518
  end
end
