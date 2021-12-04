defmodule Day03 do
    def input do
      File.stream!("./test/day03.txt")
      |> Stream.map(&String.trim/1)
    end
  
    def part1(xs) do
        xs
        |> counts()
        |> gamma()
    end
  
    def part2(xs) do
        1
    end

    defp counts(xs) do
        Enum.c
    end
  end
  
  defmodule Day03Test do
    use ExUnit.Case

    test "input" do
        assert Day03.input() |> Enum.to_list() |> length == 1000
        assert Day03.input() |> Enum.at(0) == "111110110111"
    end
  
    test "part1" do
      assert Day03.input() |> Day01.part1() == 3969000
    end
  
    # test "part2" do
    #   assert Day03.input() |> Day01.part2() == 4267809
    # end
  end
  