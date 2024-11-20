from hardware.processor import Computer
from hardware.util import *
from software.lex import Lexer
from software.parse import Parser
from software.pretty_printer import print_ast
from software.translate import Translator

def main():
    instructions = run_software()
    run_hardware(instructions)

def run_software():
    lex = Lexer()
    lres = lex.lex_file("test.as")

    parser = Parser()
    pres = parser.parse_tokens(lres)
    # print_ast(pres)

    translator = Translator()
    instructions = translator.translate(pres)
    
    return instructions

def run_hardware(instructions): 
    print("Building computer...")
    computer = Computer()

    for instruction in instructions:
        print("Adding instruction...")
        computer.add_instruction(instruction)

    while True:
        print("Press 'enter' to cycle the computer, or 'q' to quit")
        waiting = input()

        if waiting == 'q':
            break

        print("Cycling computer...")
        res = computer.cycle()
        print(f"A: {res['A']} (hex: {hex_of(res['A'])}, dec: {num_of(res['A'])})")
        print(f"D: {res['D']} (hex: {hex_of(res['D'])}, dec: {num_of(res['D'])})")
        print(f"*A: {res['*A']} (hex: {hex_of(res['*A'])}, dec: {num_of(res['*A'])})")

if __name__ == "__main__":
    main()