from shor3 import shor_alg
from ClassicalFuncs import ClassicalFuncs as CF
from CompoundGates import CompoundGates
import random


class FindFactor:
    def __init__(self, N):
        self.N = N
        self.N_left = N
        self.factors = []
        self.forbidden = []

    def found_a(self, a, button=True):
        self.N_left = self.N_left // a
        self.factors.append(a)
        if button:
            print("finding factors, {} = {}".format(self.N, self.N_left), end='')
            for num in self.factors:
                print(" x {}".format(num), end='')
            print("")

    def conclusion(self):
        print("The factors are: {} = {}".format(self.N, self.N_left), end='')
        for num in self.factors:
            print(" x {}".format(num), end='')
        print("")

    def find_one_factor(self, N=None):
        if N is None:
            N = self.N_left

        if N % 2 == 0:
            self.found_a(2)
            return 2

        a = random.randint(2, N-1)
        if CF.gcd(a, N) > 1:
            print("randomly generating {}, classically found {}'s factor {};".format(a, N, CF.gcd(a, N)))
            self.found_a(CF.gcd(a, N))
            return CF.gcd(a, N)
        # 这里其实有一个漏洞，如果这个最大公因数不是质数，那它还需要再分解

        s_r = shor_alg(a, N, L=CompoundGates.find_n(N)*2)       # 一般取精度L为2n，但可以讨论效率取舍问题
        cont_frac = CF.continued_frac(s_r)
        r_might = CF.solve_con_frac(cont_frac, return_denominator=True)
        r = None
        for k in r_might:
            if (a ** k) % N == 1:
                r = k
                break
        if r is None:
            print("Quantum ShorAlg: randomly generating a multiplier {}, trying to find its order (mod {}), but failed;"
                  .format(a, N))
            return self.find_one_factor(N=N)
        elif r % 2 != 0:
            print("Quantum ShorAlg: randomly generating a multiplier {}, found its order {} (mod {}), it's odd, "
                  "so failed;"
                  .format(a, r, N))
            return self.find_one_factor(N=N)
        elif (a ** int(r/2)) % N == N-1:
            print("Quantum ShorAlg: randomly generating a multiplier {}, found its order {} (mod {}),"
                  " {}^{}=-1(mod {}), so failed;"
                  .format(a, r, N, a, int(r/2), N))
            return self.find_one_factor(N=N)
        else:
            p_might1, p_might2 = CF.gcd(a ** int(r/2) - 1, N), CF.gcd(a ** int(r/2) + 1, N)
            if p_might1 != 1 and p_might1 != N and N % p_might1 == 0:
                print("Quantum ShorAlg: randomly generating a multiplier {}, found its order {} (mod {}),"
                      " leading to a factor {};"
                      .format(a, r, N, p_might1))
                self.found_a(p_might1)
                return p_might1
            elif p_might2 != 1 and p_might2 != N and N % p_might2 == 0:
                print("Quantum ShorAlg: randomly generating a multiplier {}, found its order {} (mod {}),"
                      " leading to a factor {};"
                      .format(a, r, N, p_might2))
                self.found_a(p_might2)
                return p_might2
            else:
                print("Quantum ShorAlg: randomly generating a multiplier {}, found its order {} (mod {}),"
                      " but can't find a factor based on it, so failed;"
                      .format(a, r, N))
                return self.find_one_factor(N=N)

    def find_factors(self):
        while not CF.prime_or_not(self.N_left):
            self.find_one_factor()
        self.conclusion()
        return self.factors
