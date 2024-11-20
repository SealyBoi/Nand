from hardware.logic_gates import *

def new_16(bit):
    res = {}
    res['0'] = bit
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

# takes a selector bit and two bits of data
# returns d0 if 0 and d1 if 1
def select(s, d1, d0):
    S = inv(s)
    A = andd(s, d1)
    B = andd(S, d0)
    return orr(A, B)

# takes a selector bit and a bit of data
# sends to c1 if 1 and c0 if 0
def switch(s, d):
    res = {}
    res['c1'] = andd(s, d)
    S = inv(s)
    res['c0'] = andd(S, d)
    return res

# takes a selector bit and two 16-digit bits
# returns d0 if 0 and d1 if 1
def select_16(s, d1, d0):
    # ensure d1 is 16-bits long
    try:
        d1['0']
    except:
        d1 = new_16(d1)
    
    # ensure d0 is 16-bits long
    try:
        d0['0']
    except:
        d0 = new_16(d0)
    
    res = {}
    res['0'] = select(s, d1['0'], d0['0'])
    res['1'] = select(s, d1['1'], d0['1'])
    res['2'] = select(s, d1['2'], d0['2'])
    res['3'] = select(s, d1['3'], d0['3'])
    res['4'] = select(s, d1['4'], d0['4'])
    res['5'] = select(s, d1['5'], d0['5'])
    res['6'] = select(s, d1['6'], d0['6'])
    res['7'] = select(s, d1['7'], d0['7'])
    res['8'] = select(s, d1['8'], d0['8'])
    res['9'] = select(s, d1['9'], d0['9'])
    res['10'] = select(s, d1['10'], d0['10'])
    res['11'] = select(s, d1['11'], d0['11'])
    res['12'] = select(s, d1['12'], d0['12'])
    res['13'] = select(s, d1['13'], d0['13'])
    res['14'] = select(s, d1['14'], d0['14'])
    res['15'] = select(s, d1['15'], d0['15'])
    return res

# takes a selector bit and two 16-digit bits
# returns d0 if 0 and d1 if 1
def select_16_to_1(s, d1, d0):
    # ensure d1 is 16-bits long
    try:
        d1['0']
    except:
        d1 = new_16(d1)
    
    # ensure d0 is 16-bits long
    try:
        d0['0']
    except:
        d0 = new_16(d0)
    
    res = select(s, d1['0'], d0['0'])
    return res