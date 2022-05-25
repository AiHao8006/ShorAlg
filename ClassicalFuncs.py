import numpy as np


def gcd(m, n):
    if not n:
        return m
    else:
        return gcd(n, m % n)


class Frac:
    def __init__(self, n, d):
        self.n = int(n)
        self.d = int(d)

    def reduction(self):
        g = gcd(self.n, self.d)
        self.n = int(self.n / g)
        self.d = int(self.d / g)
        return Frac(self.n, self.d)

    def inverse(self):
        self.n, self.d = self.d, self.n
        return Frac(self.n, self.d)

    def plus(self, n1, d1, reduc=True):
        n0, d0 = self.n, self.d
        self.d = d0 * d1
        self.n = n0 * d1 + n1 * d0
        if reduc:
            self.reduction()
        return Frac(self.n, self.d)

    def listed(self):
        return [self.n, self.d]


class ClassicalFuncs:
    def __init__(self):
        pass

    @staticmethod
    def gcd(m, n):
        return gcd(m, n)

    @staticmethod
    def continued_frac(x, n=100):
        con_frac = []
        for i in range(n):
            con_frac.append(int(x))
            if abs(x - int(x)) < 1e-5:
                return con_frac
            x = 1 / (x - int(x))
        return con_frac

    @staticmethod
    def solve_con_frac(con_frac, return_denominator=False):
        fracs = []
        for n in range(len(con_frac)):
            frac = Frac(1, 0)
            i = n
            while i >= 0:
                frac.inverse()
                frac.plus(con_frac[i], 1)
                i = i - 1
            fracs.append(frac.listed())
        if return_denominator:
            return [i[1] for i in fracs]
        else:
            return fracs

    @staticmethod
    def prime_or_not(N):
        factorial = 1
        for i in range(1, N):
            factorial = (factorial * i) % N
        if factorial == N - 1:
            return True
        else:
            return False
