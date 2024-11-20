# default send input
# if receive current, send nothing
def relay_on(c, input):
    if c == 0:
        return input
    else:
        return 0

# default send nothing
# if receive current, send input
def relay_off(c, input):
    if c == 1:
        return input
    else:
        return 0

# 0 0 - 1
# 0 1 - 1
# 1 0 - 1
# 1 1 - 0
def nand(a, b):
    c = relay_off(a, b)
    return relay_on(c, 1)

# 0 - 1
# 1 - 0
def inv(a):
    return nand(a, a)

# inverts a 16-digit bit
def inv_16(s):
    res = {}
    res['0'] = inv(s['0'])
    res['1'] = inv(s['1'])
    res['2'] = inv(s['2'])
    res['3'] = inv(s['3'])
    res['4'] = inv(s['4'])
    res['5'] = inv(s['5'])
    res['6'] = inv(s['6'])
    res['7'] = inv(s['7'])
    res['8'] = inv(s['8'])
    res['9'] = inv(s['9'])
    res['10'] = inv(s['10'])
    res['11'] = inv(s['11'])
    res['12'] = inv(s['12'])
    res['13'] = inv(s['13'])
    res['14'] = inv(s['14'])
    res['15'] = inv(s['15'])
    return res

# 0 0 - 0
# 0 1 - 0
# 1 0 - 0
# 1 1 - 1
def andd(a, b):
    res = nand(a, b)
    return inv(res)

# takes in two 16-digit bits
# returns a 16-digit bit of an 'and' comparison on each bit
def andd_16(a, b):
    res = {}
    res['0'] = andd(a['0'], b['0'])
    res['1'] = andd(a['1'], b['1'])
    res['2'] = andd(a['2'], b['2'])
    res['3'] = andd(a['3'], b['3'])
    res['4'] = andd(a['4'], b['4'])
    res['5'] = andd(a['5'], b['5'])
    res['6'] = andd(a['6'], b['6'])
    res['7'] = andd(a['7'], b['7'])
    res['8'] = andd(a['8'], b['8'])
    res['9'] = andd(a['9'], b['9'])
    res['10'] = andd(a['10'], b['10'])
    res['11'] = andd(a['11'], b['11'])
    res['12'] = andd(a['12'], b['12'])
    res['13'] = andd(a['13'], b['13'])
    res['14'] = andd(a['14'], b['14'])
    res['15'] = andd(a['15'], b['15'])
    return res

# 0 0 - 0
# 0 1 - 1
# 1 0 - 1
# 1 1 - 1
def orr(a, b):
    A = inv(a)
    B = inv(b)
    return nand(A, B)

# takes in two 16-digit bits
# returns a 16-digit bit of an 'or' comparison on each bit
def orr_16(a, b):
    res = {}
    res['0'] = orr(a['0'], b['0'])
    res['1'] = orr(a['1'], b['1'])
    res['2'] = orr(a['2'], b['2'])
    res['3'] = orr(a['3'], b['3'])
    res['4'] = orr(a['4'], b['4'])
    res['5'] = orr(a['5'], b['5'])
    res['6'] = orr(a['6'], b['6'])
    res['7'] = orr(a['7'], b['7'])
    res['8'] = orr(a['8'], b['8'])
    res['9'] = orr(a['9'], b['9'])
    res['10'] = orr(a['10'], b['10'])
    res['11'] = orr(a['11'], b['11'])
    res['12'] = orr(a['12'], b['12'])
    res['13'] = orr(a['13'], b['13'])
    res['14'] = orr(a['14'], b['14'])
    res['15'] = orr(a['15'], b['15'])
    return res

# 0 0 - 0
# 0 1 - 1
# 1 0 - 1
# 1 1 - 0
def xor(a, b):
    A = orr(a, b)
    B = nand(a, b)
    return andd(A, B)

# takes in two 16-digit bits
# returns a 16-digit bit of an 'xor' comparison on each bit
def xor_16(a, b):
    res = {}
    res['0'] = xor(a['0'], b['0'])
    res['1'] = xor(a['1'], b['1'])
    res['2'] = xor(a['2'], b['2'])
    res['3'] = xor(a['3'], b['3'])
    res['4'] = xor(a['4'], b['4'])
    res['5'] = xor(a['5'], b['5'])
    res['6'] = xor(a['6'], b['6'])
    res['7'] = xor(a['7'], b['7'])
    res['8'] = xor(a['8'], b['8'])
    res['9'] = xor(a['9'], b['9'])
    res['10'] = xor(a['10'], b['10'])
    res['11'] = xor(a['11'], b['11'])
    res['12'] = xor(a['12'], b['12'])
    res['13'] = xor(a['13'], b['13'])
    res['14'] = xor(a['14'], b['14'])
    res['15'] = xor(a['15'], b['15'])
    return res