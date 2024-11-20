from software.parse import *

class Translator:
    def __init__(self):
        self.instructions = []
        self.env = {}
        self.ci = 32768
    
    def empty_instruction(self):
        res = {}

        res['0'] = 0
        res['1'] = 0
        res['2'] = 0
        res['3'] = 0
        res['4'] = 0
        res['5'] = 0
        res['6'] = 0
        res['7'] = 0
        res['8'] = 0
        res['9'] = 0
        res['10'] = 0
        res['11'] = 0
        res['12'] = 0
        res['13'] = 0
        res['14'] = 0
        res['15'] = 0

        return res
    
    def convert_to_binary(self, num):
        return bin(num)

    def convert_to_instruction(self, num):
        bi = list(self.convert_to_binary(num))

        res = self.empty_instruction()
        res_num = 0
        for x in reversed(range(len(bi))):
            if x <= 1:
                break # 0 and 1 are '0b' in the string, so break loop if we reach it
            res[f'{res_num}'] = int(bi[x])
            res_num += 1
        
        return res

    def translate(self, ast):
        self.instructions = []

        # preload all defines and labels
        x = 0
        while x < len(ast):
            if ast[x].type == ObjType.DEFINEEXP or ast[x].type == ObjType.LABELEXP:
                self.eval(ast[x])
                ast.pop(x)
                x -= 1
            x += 1

        for node in ast:
            instruction = self.eval(node)

            if instruction != None:
                # add ci to every instruction, and remove it in assign if params are right
                bi = self.convert_to_instruction(instruction + self.ci)
                self.instructions.append(bi)
        
        return self.instructions
    
    def eval(self, node):
        match node.type:
            case ObjType.DEFINEEXP:
                return self.eval_define(node)
            case ObjType.LABELEXP:
                return self.eval_label(node)
            case ObjType.CONDJMPEXP:
                return self.eval_cond_jmp(node)
            case ObjType.JMPEXP:
                return self.eval_jmp(node)
            case ObjType.ASSIGNEXP:
                return self.eval_assign(node)
            case ObjType.OPEXP:
                return self.eval_op(node)
            case ObjType.UNARYEXP:
                return self.eval_unary(node)
            case ObjType.REGEXP:
                return self.eval_reg(node)
            case ObjType.NUMEXP:
                return self.eval_num(node)
            case ObjType.BIEXP:
                return self.eval_bi(node)
            case ObjType.HEXEXP:
                return self.eval_hex(node)
            case ObjType.IDENTEXP:
                return self.eval_hex(node)
            case _:
                raise ValueError(f"Unrecognized object type {node.type}")
    
    # Establish the defined variable in our env
    # Returns nothing
    def eval_define(self, node: DefineExp):
        address = 0
        match node.address.type:
            case ObjType.NUMEXP:
                address = self.eval_num(node.address)
            case ObjType.BIEXP:
                address = self.eval_bi(node.address)
            case ObjType.HEXEXP:
                address = self.eval_hex(node.address)
        self.env[node.ident.value] = address
        return None
    
    # Save the next instruction address in our env
    # Returns nothing
    def eval_label(self, node: LabelExp):
        address = 0
        match node.address.type:
            case ObjType.NUMEXP:
                address = self.eval_num(node.address)
            case ObjType.BIEXP:
                address = self.eval_bi(node.address)
            case ObjType.HEXEXP:
                address = self.eval_hex(node.address)
        self.env[node.ident.value] = address
        return None
    
    # Needs to decipher which condition and jmp exist
    # Returns the addition of two existing methods
    def eval_cond_jmp(self, node: CondJmpExp) -> int:
        cond = 0
        # tedious process of matching the left side of the jmp statement
        match node.cond.type:
            case ObjType.ASSIGNEXP:
                cond = self.eval_assign(node.cond)
            case ObjType.UNARYEXP:
                cond = self.eval_unary(node.cond)
            case ObjType.OPEXP:
                cond = self.eval_op(node.cond)
            case ObjType.IDENTEXP:
                cond = self.eval_ident(node.cond)
            case ObjType.NUMEXP:
                cond = self.eval_num(node.cond)
            case ObjType.BIEXP:
                cond = self.eval_bi(node.cond)
            case ObjType.HEXEXP:
                cond = self.eval_hex(node.cond)
            case ObjType.REGEXP:
                reg = 1152
                # Default to A
                match node.cond.value:
                    case 'A':
                        reg += 0
                    case 'D':
                        reg += 64
                cond = reg
        
        # Now we just grab the already established jmp statement
        jmp = self.eval_jmp(node.jmp)
        return cond + jmp

    # Needs to decipher which jmp it is
    # Returns numeric equivalent of the jmp
    def eval_jmp(self, node: JmpExp) -> int:
        match node.value:
            case 'JGT':
                return 1
            case 'JEQ':
                return 2
            case 'JLT':
                return 4
            case 'JGE':
                return 3
            case 'JLE':
                return 6
            case 'JNE':
                return 5
            case 'JMP':
                return 7
            case _:
                raise ValueError(f"Unrecognized jmp value {node.value}")

    # Needs to decipher which is the target reg and if ci needs to be subtracted or not
    # Returns the numeric equivalent of the target reg and the assignment
    def eval_assign(self, node: AssignExp) -> int:
        reg = 0
        right = 0

        for r in node.left:
            reg += self.eval_reg(r)
        
        is_num = False
        match node.right.type:
            case ObjType.NUMEXP:
                is_num = True
                right = self.eval_num(node.right)
            case ObjType.BIEXP:
                is_num = True
                right = self.eval_bi(node.right)
            case ObjType.HEXEXP:
                is_num = True
                right = self.eval_hex(node.right)
            case ObjType.OPEXP:
                right = self.eval_op(node.right)
            case ObjType.IDENTEXP:
                is_num = True
                right = self.eval_ident(node.right)
            case ObjType.REGEXP:
                reg = 1152
                # Default to A
                match node.right.value:
                    case 'A':
                        reg += 0
                    case 'D':
                        reg += 64
                right = reg
            case _:
                raise ValueError(f"Unexpected object type {node.right.type} in AssignExp")
        
        # check for if left is only A and right is a number
        if reg == 32 and is_num:
            return right - self.ci # if A is the only selection, then don't return it as it is default
        else:
            return reg + right
    
    # Needs to decipher which op and registers to return
    # Returns the numeric equivalent of the left and right operands with the op
    def eval_op(self, node: OpExp) -> int:
        op = 0
        left = 0
        right = 0

        # defaults to D-op-A
        match node.op:
            case '&':
                op = 0
            case '^':
                op = 512
            case '|':
                op = 256
            case '+':
                op = 1024
            case '-':
                op = 1536
        
        # if left is D then do not change, if it is A then swap
        match node.left.value:
            case 'D':
                left = 0
            case 'A':
                left = 64
        
        # if D or A is on the right then do not change, if it is 1 then op0
        match node.right.value:
            case 'D' | 'A':
                right = 0
            case '1':
                right = 256
        
        return op + left + right
    
    # Needs to decipher which op and register to return
    # Returns the numeric equivalent of the unary op plus the register
    def eval_unary(self, node: UnaryExp) -> int:
        op = 0
        reg = 0

        # defaults to A register
        match node.op:
            case '-':
                op = 1664
            case '~':
                op = 832
        
        # adds values necessary to create the correct instruction
        match node.right.value:
            case 'A':
                reg = 0
            case 'D':
                if op == 1664:
                    reg = 64
                else:
                    reg = -64
            case '*A':
                reg = 4096
            case '1':
                reg = 256
        
        return op + reg
    
    # Needs to manually decide which number to return based on the register
    # Returns numeric equivalent of binary instruction for target register
    def eval_reg(self, node: RegExp) -> int:
        match node.value:
            case 'A':
                return 32
            case 'D':
                return 16
            case '*A':
                return 8
            case _:
                raise ValueError(f"Unrecognized register {node.value}")

    # Returns numeric equivalent of itself
    def eval_num(self, node: NumExp) -> int:
        return int(node.value)
    
    # Returns numeric equivalent of itself
    def eval_bi(self, node) -> int:
        return int(node.value.replace("_", ""), 2)

    # Returns numeric equivalent of itself
    def eval_hex(self, node: HexExp) -> int:
        return int(node.value, 0)
    
    # If we hit here, that means we are trying to access the variable
    # Returns the environment variable
    def eval_ident(self, node: IdentExp) -> int:
        return int(self.env[node.value])