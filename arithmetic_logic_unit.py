from logic_gates import *
from arithmetics import *
from switching import *

# 16-digit bit meaning 1
one_16 = {
    '0': 1,
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
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

# takes in two bits and two 16-digit bits and selects an operation to perform
# op1 = 0, op0 = 0 'X and Y'
# op1 = 0, op0 = 1 'X or Y'
# op1 = 1, op0 = 0 'X xor Y'
# op1 = 1, op0 = 1 'invert X'
# returns a 16-digit bit
def logic_unit(op1, op0, x, y):
    xandy = andd_16(x, y)
    xory = orr_16(x, y)
    xxory = xor_16(x, y)
    invx = inv_16(x)

    resandor = select_16(op0, xory, xandy)
    resinvxxor = select_16(op0, invx, xxory)

    res = select_16(op1, resinvxxor, resandor)
    return res

# takes in two bits and two 16-digit bits and selects an operation to perform
# op1 = 0, op0 = 0 'X + Y'
# op1 = 1, op0 = 0 'X - Y'
# op1 = 0, op0 = 1 'X + 1'
# op1 = 1, op0 = 1 'X - 1'
# returns a 16-digit bit
def arithmetic_unit(op1, op0, x, y):
    d0 = y
    d1 = one_16
    Y = select_16(op0, d1, d0)

    xplus = add_16(x, Y, zero)
    xminus = sub_16(x, Y)
    res = select_16(op1, xminus, xplus)
    return res

# takes in a five bits and two 16-digit bits
# u decides between logic and arithmetic
# zx means replace left operand with 0
# sw means swap operands
# returns a 16-digit bit
def ALU(u, op1, op0, zx, sw, x, y):
    X = select_16(sw, y, x)
    Y = select_16(sw, x, y)

    X = select_16(zx, zero_16, X)

    logic = logic_unit(op1, op0, X, Y)
    arithmetic = arithmetic_unit(op1, op0, X, Y)

    res = select_16(u, arithmetic, logic)
    return res

# takes in three bits and a 16-digit bit
# compares whether it is less than, greater than, or equal to 0
# returns a 1 or 0
def condition(lt, eq, gt, x):
    xneg = is_neg_16(x)
    xzero = is_zero_16(x)

    a = andd(lt, xneg)
    b = andd(eq, xzero)
    A = orr(a, b)

    negxorzero = inv(xor(xneg, xzero))
    B = andd(gt, negxorzero)

    res = orr(A, B)
    return res