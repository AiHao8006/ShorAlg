import pyqpanda as pq
import numpy as np


class CompoundGates:
    def __init__(self, n=5):
        self.n = n

    @staticmethod
    def CARRY(qubits_4):
        Gate_set = pq.create_empty_circuit()
        Gate_set << pq.Toffoli(qubits_4[1], qubits_4[2], qubits_4[3]) << pq.CNOT(qubits_4[1], qubits_4[2]) \
        << pq.Toffoli(qubits_4[0], qubits_4[2], qubits_4[3])
        return Gate_set

    @staticmethod
    def SUM(qubits_3):
        Gate_set = pq.create_empty_circuit()
        Gate_set << pq.CNOT(qubits_3[0], qubits_3[2]) << pq.CNOT(qubits_3[1], qubits_3[2])
        return Gate_set

    def PhiADD(self, qubits, cnum, n=None, inverse=False,
               control_qubits=None):  # cbits is a list, e.g., cbits=[1,0,0,1,1]
        if n is None:
            n = self.n
        cbits = self.cnumber_to_cbits(cnum, n=n)

        Gate_set = pq.create_empty_circuit()

        for i in range(n - 1, -1, -1):  # i = n-1, n-2, ..., 0
            phi_i = 0
            for k in range(i, -1, -1):  # k = i, i-1, ..., 0
                phi_i = phi_i + 2 * np.pi / 2 ** (i + 1 - k) * cbits[k]

            if inverse:
                phi_i = -phi_i

            if control_qubits is None:
                Gate_set << pq.U1(qubits[i], phi_i)
            else:
                Gate_set << pq.U1(qubits[i], phi_i).control(control_qubits)

        return Gate_set

    def QFT(self, qubits, n=None, inverse=False):
        if n is None:
            n = self.n

        Gate_set = pq.create_empty_circuit()

        if not inverse:
            for i in range(n - 1, -1, -1):  # i = n-1, ..., 0
                Gate_set << pq.H(qubits[i])
                for k in range(i - 1, -1, -1):  # k = i-1, ..., 0
                    Gate_set << pq.CR(qubits[k], qubits[i], 2 * np.pi / 2 ** (i - k + 1))
        else:
            for i in range(n):  # i = 0, ..., n-1
                for k in range(i):  # k = 0, ..., i-1
                    Gate_set << pq.CR(qubits[k], qubits[i], 2 * np.pi / 2 ** (i - k + 1)).dagger()
                Gate_set << pq.H(qubits[i]).dagger()

        return Gate_set

    def PhiADD_MOD(self, prog, qubits, cnum, cnum_N, n=None, control_qubits=None,
                   inverse=False):  # a < N in Shor
        if n is None:
            n = self.n

        qubits_reduce = [qubits[i] for i in range(n - 1)]

        if not inverse:
            prog << self.PhiADD(qubits, cnum, n=n, control_qubits=control_qubits)
            prog << self.PhiADD(qubits, cnum_N, n=n, inverse=True)
            prog << self.QFT(qubits, n=n, inverse=True)
            prog << self.QFT(qubits_reduce, n=n-1)
            prog << self.PhiADD(qubits_reduce, cnum_N, n=n-1, control_qubits=qubits[n-1])
            prog << self.QFT(qubits_reduce, n=n-1, inverse=True)
            prog << pq.Reset(qubits[n-1])
            prog << self.QFT(qubits, n=n)

        else:
            prog << self.PhiADD(qubits, cnum, n=n, inverse=True, control_qubits=control_qubits)
            prog << self.QFT(qubits, n=n, inverse=True)
            prog << self.QFT(qubits_reduce, n=n - 1)
            prog << self.PhiADD(qubits_reduce, cnum_N, n=n - 1, control_qubits=qubits[n - 1])
            prog << self.QFT(qubits_reduce, n=n - 1, inverse=True)
            prog << pq.Reset(qubits[n - 1])
            prog << self.QFT(qubits, n=n)

        return prog

    def C_MULT_MOD(self, prog, qubits_c, qubits_x, qubits_b, cnum_a, cnum_N, n=None, inverse=False):
        if n is None:
            n = self.n
        # !!! Now, n is Shor's bit number n, so n(qubit_x)=n, n(qubit_b)=n+1

        prog << self.QFT(qubits_b, n=n + 1)
        for i in range(n):
            prog = self.PhiADD_MOD(prog, qubits_b, int(cnum_a * 2 ** i) % cnum_N, cnum_N,
                                   control_qubits=[qubits_c, qubits_x[i]], inverse=inverse, n=n + 1)
        prog << self.QFT(qubits_b, n=n + 1, inverse=True)

        return prog

    def CU(self, prog, qubits_c, qubits_x, qubits_0, cnum_a, cnum_N, n=None):
        if n is None:
            n = self.n
        # n(qubit_x)=n, n(qubit_0)=n+1

        prog = self.C_MULT_MOD(prog, qubits_c, qubits_x, qubits_0, cnum_a, cnum_N)
        for i in range(n):
            prog << pq.SWAP(qubits_0[i], qubits_x[i]).control(qubits_c)
        prog = self.C_MULT_MOD(prog, qubits_c, qubits_x, qubits_0, self.invert(cnum_a, cnum_N), cnum_N,
                               inverse=True)

        return prog

    def cnumber_to_cbits(self, cnumber, n=None):
        if n is None:
            n = self.n

        mod_array = np.zeros(n, dtype=int)
        for i in range(n):
            mod_array[i] = int(2 ** i)

        cnumber = cnumber % (mod_array * 2)
        cnumber = cnumber // mod_array
        return list(cnumber)

    def cbits_to_cnumber(self, cbits, n=None):
        if n is None:
            n = self.n

        mod_array = np.zeros(n, dtype=int)
        for i in range(n):
            mod_array[i] = int(2 ** i)

        cnumber = np.sum(np.array(cbits) * mod_array)
        return cnumber

    def gcd(self, m, n):
        if not n:
            return m
        else:
            return self.gcd(n, m % n)

    def invert(self, a, N):
        if self.gcd(a, N) != 1:
            return 0
        for i in range(N):
            if int(i * a) % N == 1:
                return i

    @staticmethod
    def find_n(N):
        N_b = list(bin(N))[2:]
        return len(N_b)
