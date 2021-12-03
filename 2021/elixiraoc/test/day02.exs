defmodule Day02 do
  def input do
    File.stream!("./test/day02.txt")
    |> Stream.map(&String.trim/1)
    |> Stream.map(&String.split(&1, " "))
    |> Stream.map(&parse/1)
  end

  defp parse(["forward", x]), do: {:forward, String.to_integer(x)}
  defp parse(["up", x]), do: {:up, String.to_integer(x)}
  defp parse(["down", x]), do: {:down, String.to_integer(x)}

  defp move({:up, z}, {x, y}), do: {x, y - z}
  defp move({:down, z}, {x, y}), do: {x, y + z}
  defp move({:forward, z}, {x, y}), do: {x + z, y}

  defp aim({:up, z}, {x, y, a}), do: {x, y, a - z}
  defp aim({:down, z}, {x, y, a}), do: {x, y, a + z}
  defp aim({:forward, z}, {x, y, a}), do: {x + z, y + a * z, a}

  def part1(xs) do
    xs
    |> Enum.reduce({0, 0}, &move(&1, &2))
    |> then(fn {x, y} -> x * y end)
  end

  def part2(xs) do
    xs
    |> Enum.reduce({0, 0, 0}, &aim(&1, &2))
    |> then(fn {x, y, _} -> x * y end)
  end
end

defmodule Day02Test do
  use ExUnit.Case

  test "loads 1000 instructions" do
    assert Enum.count(Day02.input()) == 1000
    assert Day02.input() |> Enum.at(0) == {:forward, 8}
  end

  test "part1" do
    assert Day02.input() |> Day02.part1() == 1_654_760
  end

  test "part2" do
    assert Day02.input() |> Day02.part2() == 1_956_047_400
  end
end
