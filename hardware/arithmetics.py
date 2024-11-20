from hardware.logic_gates import *

# empty 16-bit array for increment
zero_16 = {
    '0': 0,
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

zero = 0

# takes two bits and adds them
# returns the high and low
def half_adder(a, b):
    res = {}
    res['h'] = andd(a, b)
    res['l'] = xor(a, b)
    return res

# takes two bits and a carry and adds them
# returns the high and low
def full_adder(a, b, carry):
    res = {}
    A = half_adder(a, b)
    B = half_adder(A['l'], carry)
    res['h'] = orr(A['h'], B['h'])
    res['l'] = B['l']
    return res

# takes two 2-digit bits and adds them
# returns a high, low, and a carry
def multi_bit_adder(a1, a0, b1, b0, carry):
    res = {}
    A = full_adder(a0, b0, carry)
    B = full_adder(a1, b1, A['h'])
    res['c'] = B['h']
    res['s1'] = B['l']
    res['s0'] = A['l']
    return res

# takes two 16-digit bits and adds them
# returns a 16-digit bit
def add_16(a, b, carry):
    s = {}
    A = full_adder(a['0'], b['0'], carry)
    B = full_adder(a['1'], b['1'], A['h'])
    C = full_adder(a['2'], b['2'], B['h'])
    D = full_adder(a['3'], b['3'], C['h'])
    E = full_adder(a['4'], b['4'], D['h'])
    F = full_adder(a['5'], b['5'], E['h'])
    G = full_adder(a['6'], b['6'], F['h'])
    H = full_adder(a['7'], b['7'], G['h'])
    I = full_adder(a['8'], b['8'], H['h'])
    J = full_adder(a['9'], b['9'], I['h'])
    K = full_adder(a['10'], b['10'], J['h'])
    L = full_adder(a['11'], b['11'], K['h'])
    M = full_adder(a['12'], b['12'], L['h'])
    N = full_adder(a['13'], b['13'], M['h'])
    O = full_adder(a['14'], b['14'], N['h'])
    P = full_adder(a['15'], b['15'], O['h'])

    s['0'] = A['l']
    s['1'] = B['l']
    s['2'] = C['l']
    s['3'] = D['l']
    s['4'] = E['l']
    s['5'] = F['l']
    s['6'] = G['l']
    s['7'] = H['l']
    s['8'] = I['l']
    s['9'] = J['l']
    s['10'] = K['l']
    s['11'] = L['l']
    s['12'] = M['l']
    s['13'] = N['l']
    s['14'] = O['l']
    s['15'] = P['l']

    return s

# takes a 16-digit bit and increments it by 1
# returns a 16-digit bit
def inc_16(s):
    carry = inv(zero)
    return add_16(s, zero_16, carry)

# takes two 16-digit bits and subtracts them
# returns a 16-digit bit
def sub_16(a, b):
    B = inc_16(inv_16(b))
    return add_16(a, B, zero)

# takes a 16-digit bit and checks if it is equal to 0
# returns 1 or 0
def is_zero_16(s):
    res01 = orr(s['0'], s['1'])
    res23 = orr(s['2'], s['3'])
    res45 = orr(s['4'], s['5'])
    res67 = orr(s['6'], s['7'])
    res89 = orr(s['8'], s['9'])
    res1011 = orr(s['10'], s['11'])
    res1213 = orr(s['12'], s['13'])
    res1415 = orr(s['14'], s['15'])

    res02 = orr(res01, res23)
    res46 = orr(res45, res67)
    res810 = orr(res89, res1011)
    res1214 = orr(res1213, res1415)

    res04 = orr(res02, res46)
    res812 = orr(res810, res1214)

    res = orr(res04, res812)

    return inv(res)

# takes a 16-digit bit and checks if it is negative
# returns a 1 or 0
def is_neg_16(s):
    return s['15']