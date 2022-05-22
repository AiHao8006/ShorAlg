import pyqpanda as pq
import numpy as np
from CompoundGates import CompoundGates
import random


def Shor_many_run(N, L=11, run_time=100):        # L: accuracy
    G = CompoundGates(n=CompoundGates.find_n(N))

    if N % 2 == 0:
        return 2

    # a = random.randint(2, N-1)
    a = 7
    if G.gcd(a, N) != 1:
        return G.gcd(a, N)

    qpool = pq.OriginQubitPool()
    qpool.set_capacity(G.n * 2 + 3)
    qubits = qpool.qAlloc_many(G.n * 2 + 3)
    qvm = pq.CPUQVM()

    cmem = pq.OriginCMem()
    measure_cbit = cmem.cAlloc_many(1)

    def Shor_one_run():
        qvm.init_qvm()
        prog = pq.QProg()

        measure_qubit = qubits[0]
        aux_qubit = qubits[1]
        qubits_x = [qubits[i] for i in range(2, G.n + 2)]
        aux_qubits_0 = [qubits[i] for i in range(G.n + 2, G.n * 2 + 3)]

        prog << pq.X(qubits_x[0])

        def run_one_measure_qubit(k, measure):
            circuit = pq.create_empty_circuit()
            # if len(measure) > 0:   reset = bool(measure[-1])
            # else: reset = False
            # if reset:
            #     circuit << pq.X(measure_qubit)
            circuit << pq.H(measure_qubit) \
                    << G.CU(measure_qubit, qubits_x, aux_qubits_0, aux_qubit, (a**(2**(L-1-k)))%N, N)
                    # << G.CU(measure_qubit, qubits_x, aux_qubits_0, aux_qubit, (a**(2**(k)))%N, N)
            theta_k = 0
            for j in range(k):
                theta_k = theta_k + 2**(k-j) * measure[j]
            theta_k = theta_k * (-np.pi)
            circuit << pq.U1(measure_qubit, theta_k) << pq.H(measure_qubit)

            prog << circuit << pq.measure_all([0], [0]) << pq.Reset(qubit_addr=0)
            result = qvm.directly_run(prog)
            result = int(result['c0'])

            return result

        measure = []
        for k in range(L):
            result_one_measure = run_one_measure_qubit(k, measure)
            measure.append(result_one_measure)
            # print(measure[k])
        measure = G.cbits_to_cnumber(measure[::-1], n=L)
        return measure

    results_saved = []
    for i in range(run_time):
        results_saved.append(Shor_one_run())
        if i % 10 == 0:  print(i)
    qvm.finalize()
    return results_saved


if __name__ == '__main__':
    print(Shor_many_run(15))

