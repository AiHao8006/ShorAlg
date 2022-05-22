import pyqpanda as pq
import numpy as np
from CompoundGates import CompoundGates

G = CompoundGates(n=4)

if __name__ == "__main__":

    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = pq.qAlloc_many(2*G.n+3)

    x_qubit = [qubits[p] for p in range(0, G.n)]
    aux_qubits_0 = [qubits[p] for p in range(G.n, 2 * G.n + 1)]
    c_qubit = qubits[2 * G.n + 1]
    aux_qubit = qubits[2 * G.n + 2]

    prog = pq.QProg()
    prog << pq.X(x_qubit[0]) \
    << pq.X(c_qubit)
    prog << G.CU(c_qubit, x_qubit, aux_qubits_0, aux_qubit, (7**(2**3))%15, 15)
    result = pq.prob_run_dict(prog, x_qubit, -1)
    #
    # prog << G.C_MULT_MOD(c_qubit, x_qubit, aux_qubits_0, aux_qubit, 10, 21)
    # result = pq.prob_run_dict(prog, aux_qubit, -1)


    i = 0
    for key in result:
        print(i, key + " : " + str(result[key]))
        i = i + 1
    pq.finalize()
