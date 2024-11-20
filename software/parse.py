from software.lex import TokenType
from enum import Enum

class ObjType(Enum):
    DEFINEEXP = 0
    LABELEXP = 1
    CONDJMPEXP = 2
    JMPEXP = 3
    ASSIGNEXP = 4
    OPEXP = 5
    UNARYEXP = 6
    REGEXP = 7
    NUMEXP = 8
    BIEXP = 9
    HEXEXP = 10
    IDENTEXP = 11

class DefineExp:
    def __init__(self, ident, address):
        self.ident = ident
        self.address = address
        self.type = ObjType.DEFINEEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}DefineExp:
{tabs}{self.ident.format(i + 1)}
{tabs}{self.address.format(i + 1)}
"""

class LabelExp:
    def __init__(self, ident, address):
        self.ident = ident
        self.address = address
        self.type = ObjType.LABELEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}LabelExp:
{tabs}{self.ident.format(i + 1)}
{tabs}{self.address.format(i + 1)}
"""

class CondJmpExp:
    def __init__(self, cond, jmp):
        self.cond = cond
        self.jmp = jmp
        self.type = ObjType.CONDJMPEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}CondJmpExp:
{tabs}{self.cond.format(i + 1)}
{tabs}{self.jmp.format(i + 1)}
"""

class JmpExp:
    def __init__(self, value):
        self.value = value
        self.type = ObjType.JMPEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}JmpExp:
\t{tabs}{self.value}
"""

class AssignExp:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.type = ObjType.ASSIGNEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        reglist = list(map(lambda l: l.format(i + 1), self.left))
        regs = ""
        for reg in reglist:
            regs += reg
        
        return f"""{tabs}AssignExp:
{tabs}{regs}
{tabs}{self.right.format(i + 1)}
"""

class OpExp:
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op
        self.type = ObjType.OPEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}OpExp:
{tabs}{self.left.format(i + 1)}
{tabs}{self.right.format(i + 1)}
\t{tabs}{self.op}
"""

class UnaryExp:
    def __init__(self, right, op):
        self.right = right
        self.op = op
        self.type = ObjType.UNARYEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}UnaryExp:
{tabs}{self.right.format(i + 1)}
\t{tabs}{self.op}
"""

class RegExp:
    def __init__(self, value):
        self.value = value
        self.type = ObjType.REGEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}RegExp:
\t{tabs}{self.value}
"""

class NumExp:
    def __init__(self, value):
        self.value = value
        self.type = ObjType.NUMEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}NumExp:
\t{tabs}{self.value}
"""

class BiExp:
    def __init__(self, value):
        self.value = value
        self.type = ObjType.BIEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}BiExp:
\t{tabs}{self.value}
"""

class HexExp:
    def __init__(self, value):
        self.value = value
        self.type = ObjType.HEXEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}HexExp:
\t{tabs}{self.value}
"""

class IdentExp:
    def __init__(self, value):
        self.value = value
        self.type = ObjType.IDENTEXP
    
    def format(self, i):
        tabs = ""
        for x in range(i):
            tabs += "\t"
        
        return f"""{tabs}IdentExp:
\t{tabs}{self.value}
"""

class Parser:
    def __init__(self):
        self.ast_tree = []
        self.curr = 0
        self.tokens = []
        self.line = 1
    
    def runtime_error(self, error):
        raise ValueError(error)
    
    def get_curr(self):
        return self.tokens[self.curr]
    
    def get_next(self):
        return self.tokens[self.curr + 1]
    
    def advance(self):
        self.curr += 1
    
    def eat(self):
        self.advance()
        return self.get_curr()
    
    def match(self, type):
        return self.get_curr().type == type
    
    def match_next(self, type):
        if self.curr + 1 >= len(self.tokens):
            return False
        
        return self.get_next().type == type
    
    def expect(self, type):
        if self.get_curr().type == type:
            return True
        else:
            self.runtime_error(f"Expected token of type {type} but got {self.get_curr().type}. Instruction: {self.line}")
    
    def expect_one(self, types):
        for type in types:
            if self.get_curr().type == type:
                return True
        
        self.runtime_error(f"Expected one of these types {types} but got {self.get_curr().type}. Instruction: {self.line}")

    def parse_tokens(self, tokens):
        self.ast_tree = []
        self.tokens = tokens
        self.line = 0

        while self.curr < len(self.tokens):
            self.ast_tree.append(self.parse_token())
            self.advance()
            self.line += 1
        
        return self.ast_tree

    def parse_token(self):
        return self.parse_define()
    
    def parse_define(self):
        if self.match(TokenType.DEFINE):
            self.advance()
            ident = self.parse_name()
            self.advance()

            self.expect_one([TokenType.NUM, TokenType.BI, TokenType.HEX])
            return DefineExp(ident, self.parse_num())
        
        return self.parse_label()

    def parse_label(self):
        if self.match(TokenType.LABEL):
            self.advance()

            self.expect(TokenType.IDENT)
            ident = self.parse_name()
            return LabelExp(ident, NumExp(self.line + 1))
        
        return self.parse_cond_jmp()
    
    def parse_cond_jmp(self):
        left = self.parse_jmp()

        if self.match_next(TokenType.SEMI):
            self.advance() # advance to semi
            self.advance() # advance past semi
            self.expect(TokenType.JMP)
            jmp = self.parse_jmp()
            return CondJmpExp(left, jmp)
        
        return left

    def parse_jmp(self):
        if self.match(TokenType.JMP):
            return JmpExp(self.get_curr().lexeme)
        
        return self.parse_assign()
    
    def parse_assign(self):
        left = self.parse_unary()
        regs = []
        regs.append(left)

        while self.match_next(TokenType.COMMA):
            self.advance() # move to comma
            self.advance() # move past comma
            self.expect(TokenType.REG)
            regs.append(self.parse_reg())
        
        if self.match_next(TokenType.EQ):
            self.advance() # move to eq
            self.advance() # move past eq
            right = self.parse_unary()
            return AssignExp(regs, right)
        
        return left
            
    
    def parse_unary(self):
        if self.match(TokenType.MINUS) | self.match(TokenType.NEG):
            op = self.get_curr().lexeme
            self.advance()
            return UnaryExp(self.parse_num(), op)
        
        return self.parse_op()
    
    def parse_op(self):
        left = self.parse_name()

        if self.match_next(TokenType.OP) | self.match_next(TokenType.MINUS):
            self.advance()
            op = self.get_curr().lexeme
            self.advance()

            right = self.parse_num()
            return OpExp(left, right, op)
        
        return left

    def parse_name(self):
        if self.match(TokenType.IDENT):
            return IdentExp(self.get_curr().lexeme)
        
        return self.parse_num()
    
    def parse_num(self):
        if self.match(TokenType.NUM):
            return NumExp(self.get_curr().lexeme)
        elif self.match(TokenType.BI):
            return BiExp(self.get_curr().lexeme)
        elif self.match(TokenType.HEX):
            return HexExp(self.get_curr().lexeme)

        return self.parse_reg()
    
    def parse_reg(self):
        star_add = ""
        if self.match(TokenType.STAR):
            star_add = self.get_curr().lexeme
            self.advance()
        
        self.expect(TokenType.REG)
        tok = star_add + self.get_curr().lexeme
        return RegExp(tok)
    