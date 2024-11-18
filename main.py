from logic_gates import *
from arithmetics import *
from switching import *
from arithmetic_logic_unit import *
from memory import *
from processor import *
from util import *

a = {
    '0': 0,
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 1,
    '6': 0,
    '7': 1,
    '8': 1,
    '9': 0,
    '10': 1,
    '11': 0,
    '12': 0,
    '13': 0,
    '14': 0,
    '15': 0,
}

b = {
    '0': 0,
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 1,
    '5': 0,
    '6': 0,
    '7': 1,
    '8': 0,
    '9': 0,
    '10': 1,
    '11': 0,
    '12': 0,
    '13': 0,
    '14': 0,
    '15': 1,
}

c = {
    '0': 1,
    '1': 1,
    '2': 0,
    '3': 0,
    '4': 1,
    '5': 0,
    '6': 0,
    '7': 0,
    '8': 0,
    '9': 0,
    '10': 0,
    '11': 0,
    '12': 0,
    '13': 0,
    '14': 0,
    '15': 0,
}

d = {
    '0': 0,
    '1': 0,
    '2': 0,
    '3': 1,
    '4': 0,
    '5': 0,
    '6': 1,
    '7': 1,
    '8': 0,
    '9': 0,
    '10': 1,
    '11': 0,
    '12': 0,
    '13': 0,
    '14': 0,
    '15': 1,
}

e = {
    '0': 0,
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 1,
    '6': 0,
    '7': 1,
    '8': 0,
    '9': 0,
    '10': 1,
    '11': 0,
    '12': 1,
    '13': 0,
    '14': 0,
    '15': 1,
}

instructions = [a, b, c, d, e]

def main():
    print("Building computer...")
    computer = Computer()

    for instruction in instructions:
        print("Adding instruction a...")
        computer.add_instruction(instruction)

    while True:
        print("Press enter to cycle the computer")
        waiting = input()
        print("Cycling computer...")
        res = computer.cycle()
        print(f"A: {res['A']} (hex: {hex_of(res['A'])}, dec: {num_of(res['A'])})")
        print(f"D: {res['D']} (hex: {hex_of(res['D'])}, dec: {num_of(res['D'])})")
        print(f"*A: {res['*A']} (hex: {hex_of(res['*A'])}, dec: {num_of(res['*A'])})")

if __name__ == "__main__":
    main()