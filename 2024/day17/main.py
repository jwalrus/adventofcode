import sys


def main():
    with open(sys.argv[1]) as fh:
        raw_input = fh.read().splitlines()
        A = int(raw_input[0].split(": ")[-1])
        B = int(raw_input[1].split(": ")[-1])
        C = int(raw_input[2].split(": ")[-1])
        program = [int(c) for c in raw_input[-1].split(": ")[-1].split(",")]
        print(A, B, C, program)
        print("part1:", ",".join(map(str, part1(A, B, C, program))))
        print("part2:", part2(A, B, C, program))

def combo(A, B, C, operand):
    if operand == 4:
        return A
    if operand == 5:
        return B
    if operand == 6:
        return C
    return operand

def part1(A, B, C, program):
    output = []
    i_pointer = 0
    update_pointer = True

    while i_pointer + 1 <= len(program) - 1:
        opcode, operand = program[i_pointer], program[i_pointer + 1]
        match opcode:
            case 0:
                A = A // 2**combo(A, B, C, operand)
            case 1:
                B = B ^ operand
            case 2:
                B = combo(A, B, C, operand) % 8
            case 3:
                if A != 0:
                    i_pointer = operand if A != 0 else i_pointer
                    update_pointer = False
            case 4:
                B = B ^ C
            case 5:
                output.append(combo(A, B, C, operand) % 8)
            case 6:
                B = A // 2**combo(A, B, C, operand)
            case 7:
                C = A // 2**combo(A, B, C, operand)

        # print(i_pointer, opcode, operand, A, B, C, output)
        # input()
        if update_pointer:
            i_pointer = i_pointer + 2
        else:
            update_pointer = True

    return output


def part2(A, B, C, program):
    # wow: credit to https://www.reddit.com/r/adventofcode/comments/1hg38ah/comment/m2gny5k/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    A = 0
    for n in range(1, len(program) + 1):
        AA = A << 3
        while True:
            out = part1(AA, B, C, program)
            if out[-n:] == program[-n:]:
                A = AA
                break
            AA += 1
    return A



if __name__ == '__main__':
    main()