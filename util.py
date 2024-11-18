# print the 16-digit bit as a hex code
def hex_of(s):
    num = num_of(s)
    return hex(num)

# print the 16-digit bit as binary
def bi_of(s):
    res = ""
    for x in range(16):
        res = str(s[f'{x}']) + res
    return res

# print the 16-digit bit as a number
def num_of(s):
    pow = 1
    res = 0
    for x in range(16):
        res += s[f'{x}'] * pow
        pow *= 2
    return res