import pyqpanda as pq
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from CompoundGates_Reset import CompoundGates

matplotlib.use('TKAgg')


def shor_alg(a, N, L=11):          # L: num of virtual measurement qubits
    G = CompoundGates(n=CompoundGates.find_n(N))
    # N must be an odd number, guaranteed by classical procedures.
    # a = random.randint(2, N-1), and gcd(a, N) != 1, guaranteed by classical procedures.

    pq.init(pq.QMachineType.CPU)
    qubits = pq.qAlloc_many(2*G.n+2)
    cbit_measure = pq.cAlloc_many(1)

    qubits_x = [qubits[p] for p in range(0, G.n)]
    qubits_0 = [qubits[p] for p in range(G.n, 2 * G.n + 1)]
    qubit_measure = qubits[2 * G.n + 1]

    prog = pq.create_empty_qprog()

    # initial |x> to |1>
    prog << pq.X(qubits_x[0])

    measured_resultes = np.zeros(L, dtype=int)
    for j in range(L):
        prog << pq.H(qubit_measure)
        prog = G.CU(prog, qubit_measure, qubits_x, qubits_0, (a ** (2 ** (L - 1 - j))) % N, N)

        theta_j = 0
        for k in range(j):          # k = 0, ..., k, ..., j-1       # R_{j+1}, ..., R_{j+1-k}, ..., R_2
            theta_j = theta_j + measured_resultes[k] * (-2 * np.pi) / 2 ** (j-k+1)
        prog << pq.U1(qubit_measure, theta_j) << pq.H(qubit_measure)

        # measure
        prog << pq.Measure(qubits[2 * G.n + 1], cbit_measure[0])
        result = pq.directly_run(prog)
        measured_resultes[j] = int(result['c0'])

        # reset
        prog << pq.Reset(qubit_measure)

    pq.finalize()
    return G.cbits_to_cnumber(measured_resultes, n=L) / 2**L


if __name__ == "__main__":
    nums_statistics = []
    for i in range(100):
        num = shor_alg(7, 15, 11)
        nums_statistics.append(num)
        if i % 10 == 0: print("进度：{}/100".format(i))

    print(nums_statistics)
    plt.hist(nums_statistics, bins=41, edgecolor='r', range=[0, 1])
    plt.show()

