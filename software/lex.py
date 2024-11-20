from enum import Enum
import os

# token object to save each word as
class Token:
    def __init__(self, lexeme, type):
        self.lexeme = lexeme
        self.type = type

# types of tokens we can save
class TokenType(Enum):
    STAR = 0
    REG = 1
    COMMA = 2
    EQ = 3
    NUM = 4
    BI = 5
    HEX = 6
    NEG = 7
    SEMI = 8
    JMP = 9
    DEFINE = 10
    LABEL = 11
    IDENT = 12
    OP = 13
    MINUS = 14

class Lexer:
    def __init__(self):
        self.tokens = []
        self.curr = 0
        self.next = 1
        self.dump = []

    # open and read a file
    # save a list of the tokens in the file and return it
    def lex_file(self, file_name):
        # path handling
        path = __file__
        dir = os.path.dirname(path) + "\\tests"
        os.chdir(dir)

        # open file in a read state
        file = open(file_name, "r")

        # initialize list of tokens
        self.tokens = []

        # loop through every line in file and tokenize
        self.dump = list(file.read())

        while self.curr < len(self.dump):
            tok = self.tokenize()
            if tok != None:
                self.tokens.append(tok)
            self.advance()

        # close the file when done
        file.close()

        # return token list
        return self.tokens
    
    def advance(self):
        self.curr += 1
        self.next += 1
    
    def eat(self):
        self.advance()
        return self.get_curr()
    
    def get_curr(self):
        tok = self.dump[self.curr]
        return tok
    
    def get_next(self):
        tok = self.dump[self.next]
        return tok
    
    def isNum(self, str):
        return str.isnumeric()

    def isAlNum(self, str):
        return str.isalnum()
    
    def atEnd(self):
        return self.next >= len(self.dump)

    def tokenize(self):
        tok = self.get_curr()

        match tok:
            # skip any whitespace
            case ' ' | '\n' | '\t' | '\r':
                return None
            # skip comment lines
            case '#':
                # while not at a new line, skip chars
                while self.get_curr() != '\n' and not self.atEnd():
                    self.advance()
                return None
            case '*':
                return Token(tok, TokenType.STAR)
            case ',':
                return Token(tok, TokenType.COMMA)
            case '=':
                return Token(tok, TokenType.EQ)
            case '+' | '&' | '|':
                return Token(tok, TokenType.OP)
            case '-':
                return Token(tok, TokenType.MINUS)
            case '~':
                return Token(tok, TokenType.NEG)
            case ';':
                return Token(tok, TokenType.SEMI)
            case 'J':
                # eat next to numbers and add to jmp string
                jmp = tok + self.eat() + self.eat()
                return Token(jmp, TokenType.JMP)
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                if tok == '0' and self.get_next().lower() == 'x':
                    # add 0x to the string
                    hex_num = tok + self.eat()
                    # advance tok past x
                    tok = self.eat()
                    # until num ends, continue to eat
                    while self.isAlNum(tok) and not self.atEnd():
                        hex_num += tok
                        tok = self.eat()
                    
                    # add final num
                    if self.isAlNum(tok):
                        hex_num += tok

                    return Token(hex_num, TokenType.HEX)
                elif tok == '0' and self.get_next().lower() == 'b':
                    # add 0b to the string
                    bi_num = tok + self.eat()
                    # advance tok past b
                    tok = self.eat()
                    # until num ends, continue to eat
                    while (self.isNum(tok) or tok == '_') and not self.atEnd():
                        bi_num += tok
                        tok = self.eat()
                    
                    # add final num
                    if self.isNum(tok) or tok == '_':
                        bi_num += tok
                    
                    return Token(bi_num, TokenType.BI)
                else:
                    # add all numbers to a string
                    num = ""
                    while self.isNum(tok) and not self.atEnd():
                        num += tok
                        tok = self.eat()
                    
                    # add final num
                    if self.isNum(tok):
                        num += tok
                    
                    return Token(num, TokenType.NUM)
            case _:
                # add this character to the list to try and read it
                leftover = tok
                # until we find whitespace, eat
                while not self.atEnd() and (self.isAlNum(self.get_next()) or self.get_next() == '_'):
                    tok = self.eat()
                    leftover += tok
                
                # list of reserved keywords that it could potentially match
                match leftover.upper():
                    case 'DEFINE':
                        return Token(leftover, TokenType.DEFINE)
                    case 'LABEL':
                        return Token(leftover, TokenType.LABEL)
                    case 'A' | 'D':
                        return Token(leftover, TokenType.REG)
                    case _:
                        return Token(leftover, TokenType.IDENT)
