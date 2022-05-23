import pyqpanda as pq
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from CompoundGates import CompoundGates

matplotlib.use('TKAgg')


def qpe_1qubit(L=11):          # L: num of virtual measurement qubits
    G = CompoundGates()

    pq.init(pq.QMachineType.CPU)
    qubits = pq.qAlloc_many(2)
    cbit_measure = pq.cAlloc_many(1)

    qubit_measure = qubits[0]
    qubit_x = qubits[1]

    prog = pq.create_empty_qprog()

    # initial |x> to |1>
    prog << pq.X(qubit_x)

    measured_resultes = np.zeros(L, dtype=int)
    for j in range(L):
        prog << pq.H(qubit_measure)
        # prog << pq.U1(qubit_x, (0.3*(2**j)) * np.pi).control(qubit_measure)
        prog << pq.U1(qubit_x, (0.5*(2**(L-1-j))) * np.pi).control(qubit_measure)

        theta_j = 0
        for k in range(j):          # k = 0, ..., k, ..., j-1       # R_{j+1}, ..., R_{j+1-k}, ..., R_2
            theta_j = theta_j + measured_resultes[k] * (-2 * np.pi) / 2 ** (j-k+1)
        prog << pq.U1(qubit_measure, theta_j) << pq.H(qubit_measure)

        # measure
        prog << pq.Measure(qubits[0], cbit_measure[0])
        result = pq.directly_run(prog)
        measured_resultes[j] = int(result['c0'])
        # print(measured_resultes)

        # reset
        prog << pq.Reset(qubit_measure)

    pq.finalize()
    return G.cbits_to_cnumber(measured_resultes, n=L), G.cbits_to_cnumber(measured_resultes[::-1], n=L)
    # theoretically, don't need to inverse.


if __name__ == "__main__":
    L = 15

    nums_statistics = []
    nums_statistics_inverse = []
    for i in range(300):
        num, num_inverse = qpe_1qubit(L)
        nums_statistics.append(num / 2**L)
        nums_statistics_inverse.append(num_inverse / 2**L)
        if i % 100 == 0: print("进度：{}".format(i))

    # print(nums_statistics)
    # print(nums_statistics_inverse)

    plt.hist(nums_statistics, bins=51, edgecolor='r', range=[0, 1])
    plt.show()

    plt.hist(nums_statistics_inverse, bins=51, edgecolor='r', range=[0, 1])
    plt.show()

