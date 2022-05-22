import pyqpanda as pq
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from CompoundGates import CompoundGates

matplotlib.use('TKAgg')


def shor_alg(a, N, L=11):          # L: num of virtual measurement qubits
    G = CompoundGates(n=CompoundGates.find_n(N))
    # N must be an odd number, guaranteed by classical procedures.
    # a = random.randint(2, N-1), and gcd(a, N) != 1, guaranteed by classical procedures.

    pq.init(pq.QMachineType.CPU)
    qubits = pq.qAlloc_many(2*G.n+3)
    cbit_measure = pq.cAlloc_many(1)

    qubits_x = [qubits[p] for p in range(0, G.n)]
    qubits_0 = [qubits[p] for p in range(G.n, 2 * G.n + 1)]
    qubit_measure = qubits[2 * G.n + 1]
    qubit_aux = qubits[2 * G.n + 2]

    prog = pq.create_empty_qprog()

    # initial |x> to |1>
    prog << pq.X(qubits_x[0])

    measured_resultes = np.zeros(L, dtype=int)
    for j in range(L):
        prog << pq.H(qubit_measure)
        prog << G.CU(qubit_measure, qubits_x, qubits_0, qubit_aux, (a ** (2 ** (L - 1 - j))) % N, N)
        # prog << G.CU(qubit_measure, qubits_x, qubits_0, qubit_aux, ((a ** 2) ** (L - 1 - j)) % N, N)
        # prog << G.CU(qubit_measure, qubits_x, qubits_0, qubit_aux, (a ** (2 ** j)) % N, N)

        theta_j = 0
        for k in range(j):          # k = 0, ..., k, ..., j-1       # R_{j+1}, ..., R_{j+1-k}, ..., R_2
            theta_j = theta_j + measured_resultes[k] * (-2 * np.pi) / 2 ** (j-k+1)
        prog << pq.U1(qubit_measure, theta_j) << pq.H(qubit_measure)

        # measure
        prog << pq.Measure(qubits[2 * G.n + 1], cbit_measure[0])
        result = pq.directly_run(prog)
        measured_resultes[j] = int(result['c0'])
        # print(measured_resultes)

        # reset
        prog << pq.Reset(qubit_measure)

    pq.finalize()
    return G.cbits_to_cnumber(measured_resultes, n=L)
    # G.cbits_to_cnumber(measured_resultes[::-1], n=L)


if __name__ == "__main__":
    nums_statistics = []
    # nums_statistics_inverse = []
    for i in range(100):
        num = shor_alg(7, 15, 11)
        nums_statistics.append(num / 2**11)
        # nums_statistics_inverse.append(num_inverse / 2**11)
        if i % 10 == 0: print("进度：{}/100".format(i))

    print(nums_statistics)
    # print(nums_statistics_inverse)

    plt.hist(nums_statistics, bins=21, edgecolor='r', range=[0, 1])
    plt.show()

    # plt.hist(nums_statistics_inverse, bins=21, edgecolor='r', range=[0, 1])
    # plt.show()

