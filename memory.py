from logic_gates import *
from arithmetics import *
from switching import *

# takes in two bits
# latches onto an output
# returns one bit
class SR_Latch:
    def __init__(self):
        self.latch_val = 0
    
    def process(self, s, r):
        R = inv(r)

        a = andd(s, R)

        b = andd(s, r)
        B = orr(R, b)

        c = andd(B, self.latch_val)
        C = orr(a, c)
        self.latch_val = C
        return C

# takes in two bits
# stores a value when st is true, and returns prev otherwise
# returns one bit
class D_Latch:
    def __init__(self):
        self.sr_latch = SR_Latch()
        self.latch_val = 0

    def process(self, st, d):
        d1 = d
        d0 = self.sr_latch.process(self.latch_val, inv(self.latch_val))

        res = select(st, d1, d0)
        self.latch_val = res
        return res

# takes in three bits
# runs on a clock cycle and updates when cl changes
# returns one bit
class Data_Flip_Flop:
    def __init__(self):
        self.d_latch1 = D_Latch()
        self.d_latch2 = D_Latch()
    
    def process(self, st, d, cl):
        a = andd(st, cl)
        A = self.d_latch1.process(a, d)

        b = inv(cl)
        B = self.d_latch2.process(b, A)

        return select(cl, B, A)

# takes in two bits and a 16-digit bit
# stores a 16-digit bit in memory
# returns a 16-digit bit
class Register:
    def __init__(self):
        self.dff0 = Data_Flip_Flop()
        self.dff1 = Data_Flip_Flop()
        self.dff2 = Data_Flip_Flop()
        self.dff3 = Data_Flip_Flop()
        self.dff4 = Data_Flip_Flop()
        self.dff5 = Data_Flip_Flop()
        self.dff6 = Data_Flip_Flop()
        self.dff7 = Data_Flip_Flop()
        self.dff8 = Data_Flip_Flop()
        self.dff9 = Data_Flip_Flop()
        self.dff10 = Data_Flip_Flop()
        self.dff11 = Data_Flip_Flop()
        self.dff12 = Data_Flip_Flop()
        self.dff13 = Data_Flip_Flop()
        self.dff14 = Data_Flip_Flop()
        self.dff15 = Data_Flip_Flop()
    
    def process(self, st, d, cl):
        s = {}
        
        s['0'] = self.dff0.process(st, d['0'], cl)
        s['1'] = self.dff1.process(st, d['1'], cl)
        s['2'] = self.dff2.process(st, d['2'], cl)
        s['3'] = self.dff3.process(st, d['3'], cl)
        s['4'] = self.dff4.process(st, d['4'], cl)
        s['5'] = self.dff5.process(st, d['5'], cl)
        s['6'] = self.dff6.process(st, d['6'], cl)
        s['7'] = self.dff7.process(st, d['7'], cl)
        s['8'] = self.dff8.process(st, d['8'], cl)
        s['9'] = self.dff9.process(st, d['9'], cl)
        s['10'] = self.dff10.process(st, d['10'], cl)
        s['11'] = self.dff11.process(st, d['11'], cl)
        s['12'] = self.dff12.process(st, d['12'], cl)
        s['13'] = self.dff13.process(st, d['13'], cl)
        s['14'] = self.dff14.process(st, d['14'], cl)
        s['15'] = self.dff15.process(st, d['15'], cl)

        return s

# takes in two bits and a 16-digit bit
# increments the value by 1 every clock cycle
# returns a 16-digit bit
class Counter:
    def __init__(self):
        self.reg = Register()
        self.latch_val = zero_16

    def process(self, st, x, cl):
        d1 = x
        d0 = inc_16(self.latch_val)

        X = select_16(st, d1, d0)

        res = self.reg.process(cl, X, cl)
        self.latch_val = res
        return res

# takes in three bits and a 16-digit bit
# ad means address
# returns a 16-digit bit
class RAM:
    def __init__(self):
        self.reg0 = Register()
        self.reg1 = Register()
    
    def process(self, ad, st, x, cl):
        dest = switch(ad, st)

        reg0_ret = self.reg0.process(dest['c0'], x, cl)
        reg1_ret = self.reg1.process(dest['c1'], x, cl)

        return select_16(ad, reg1_ret, reg0_ret)

# creates a 16-address RAM
# returns the selected RAM address
# this is where we have to 'cheat' a bit
# we can't go down the path that we aren't meant to use, as this will override it anyways
class RAM_16:
    def __init__(self):
        self.ram0 = RAM()
        self.ram1 = RAM()
        self.ram2 = RAM()
        self.ram3 = RAM()
        self.ram4 = RAM()
        self.ram5 = RAM()
        self.ram6 = RAM()
        self.ram7 = RAM()
    
    def process(self, ad, st, x, cl):
        destmax = switch(ad['3'], st)

        dest0123 = switch(ad['2'], destmax['c0'])
        dest4567 = switch(ad['2'], destmax['c1'])

        dest01 = switch(ad['1'], dest0123['c0'])
        dest23 = switch(ad['1'], dest0123['c1'])
        dest45 = switch(ad['1'], dest4567['c0'])
        dest67 = switch(ad['1'], dest4567['c1'])

        res01 = select_16(ad['1'], self.ram1.process(ad['0'], dest01['c1'], x, cl), self.ram0.process(ad['0'], dest01['c0'], x, cl))
        res23 = select_16(ad['1'], self.ram3.process(ad['0'], dest23['c1'], x, cl), self.ram2.process(ad['0'], dest23['c0'], x, cl))
        res45 = select_16(ad['1'], self.ram5.process(ad['0'], dest45['c1'], x, cl), self.ram4.process(ad['0'], dest45['c0'], x, cl))
        res67 = select_16(ad['1'], self.ram7.process(ad['0'], dest67['c1'], x, cl), self.ram6.process(ad['0'], dest67['c0'], x, cl))

        res0123 = select_16(ad['2'], res23, res01)
        res4567 = select_16(ad['2'], res67, res45)

        return select_16(ad['3'], res4567, res0123)

class RAM_64:
    def __init__(self):
        self.ram0 = RAM_16()
        self.ram1 = RAM_16()
        self.ram2 = RAM_16()
        self.ram3 = RAM_16()
    
    def process(self, ad, st, x, cl):
        destmax = switch(ad['5'], st)

        dest0 = switch(ad['4'], destmax['c0'])
        dest1 = switch(ad['4'], destmax['c1'])

        res0 = select_16(ad['4'], self.ram1.process(ad, dest0['c1'], x, cl), self.ram0.process(ad, dest0['c0'], x, cl))
        res1 = select_16(ad['4'], self.ram3.process(ad, dest1['c1'], x, cl), self.ram2.process(ad, dest1['c0'], x, cl))

        res = select_16(ad['5'], res1, res0)

        return res

class RAM_256:
    def __init__(self):
        self.ram0 = RAM_64()
        self.ram1 = RAM_64()
        self.ram2 = RAM_64()
        self.ram3 = RAM_64()
    
    def process(self, ad, st, x, cl):
        destmax = switch(ad['7'], st)

        dest0 = switch(ad['6'], destmax['c0'])
        dest1 = switch(ad['6'], destmax['c1'])

        res0 = select_16(ad['6'], self.ram1.process(ad, dest0['c1'], x, cl), self.ram0.process(ad, dest0['c0'], x, cl))
        res1 = select_16(ad['6'], self.ram3.process(ad, dest1['c1'], x, cl), self.ram2.process(ad, dest1['c0'], x, cl))

        res = select_16(ad['7'], res1, res0)

        return res

class RAM_1024:
    def __init__(self):
        self.ram0 = RAM_256()
        self.ram1 = RAM_256()
        self.ram2 = RAM_256()
        self.ram3 = RAM_256()
    
    def process(self, ad, st, x, cl):
        destmax = switch(ad['9'], st)

        dest0 = switch(ad['8'], destmax['c0'])
        dest1 = switch(ad['8'], destmax['c1'])

        res0 = select_16(ad['8'], self.ram1.process(ad, dest0['c1'], x, cl), self.ram0.process(ad, dest0['c0'], x, cl))
        res1 = select_16(ad['8'], self.ram3.process(ad, dest1['c1'], x, cl), self.ram2.process(ad, dest1['c0'], x, cl))

        res = select_16(ad['9'], res1, res0)

        return res

class RAM_4096:
    def __init__(self):
        self.ram0 = RAM_1024()
        self.ram1 = RAM_1024()
        self.ram2 = RAM_1024()
        self.ram3 = RAM_1024()
    
    def process(self, ad, st, x, cl):
        destmax = switch(ad['11'], st)

        dest0 = switch(ad['10'], destmax['c0'])
        dest1 = switch(ad['10'], destmax['c1'])

        res0 = select_16(ad['10'], self.ram1.process(ad, dest0['c1'], x, cl), self.ram0.process(ad, dest0['c0'], x, cl))
        res1 = select_16(ad['10'], self.ram3.process(ad, dest1['c1'], x, cl), self.ram2.process(ad, dest1['c0'], x, cl))

        res = select_16(ad['11'], res1, res0)

        return res

class RAM_16384:
    def __init__(self):
        self.ram0 = RAM_4096()
        self.ram1 = RAM_4096()
        self.ram2 = RAM_4096()
        self.ram3 = RAM_4096()
    
    def process(self, ad, st, x, cl):
        destmax = switch(ad['13'], st)

        dest0 = switch(ad['12'], destmax['c0'])
        dest1 = switch(ad['12'], destmax['c1'])

        res0 = select_16(ad['12'], self.ram1.process(ad, dest0['c1'], x, cl), self.ram0.process(ad, dest0['c0'], x, cl))
        res1 = select_16(ad['12'], self.ram3.process(ad, dest1['c1'], x, cl), self.ram2.process(ad, dest1['c0'], x, cl))

        res = select_16(ad['13'], res1, res0)

        return res

class RAM_MAX:
    def __init__(self):
        self.ram0 = RAM_16384()
        self.ram1 = RAM_16384()
        self.ram2 = RAM_16384()
        self.ram3 = RAM_16384()
    
    def process(self, ad, st, x, cl):
        destmax = switch(ad['15'], st)

        dest0 = switch(ad['14'], destmax['c0'])
        dest1 = switch(ad['14'], destmax['c1'])

        res0 = select_16(ad['14'], self.ram1.process(ad, dest0['c1'], x, cl), self.ram0.process(ad, dest0['c0'], x, cl))
        res1 = select_16(ad['14'], self.ram3.process(ad, dest1['c1'], x, cl), self.ram2.process(ad, dest1['c0'], x, cl))

        res = select_16(ad['15'], res1, res0)

        return res