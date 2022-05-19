import pyqpanda as pq
import numpy as np
from CompoundGates import CompoundGates

G = CompoundGates(n=5)

if __name__ == "__main__":

    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits_all = pq.qAlloc_many(13)
    c_qubit = qubits_all[0]
    aux_qubit = qubits_all[1]
    x_qubit = [qubits_all[i] for i in range(2, 7)]
    aux_qubits_0 = [qubits_all[i] for i in range(7, 13)]

    prog = pq.QProg()
    prog << pq.X(x_qubit[1]) << pq.X(x_qubit[0]) \
    << pq.X(c_qubit) \
    << G.CU(c_qubit, x_qubit, aux_qubits_0, aux_qubit, 10, 21)
    # << G.C_MULT_MOD(c_qubit, x_qubit, aux_qubits_0, aux_qubit, 10, 21)

    result = pq.prob_run_dict(prog, aux_qubits_0, -1)
    for key in result:
        print(key + " : " + str(result[key]))
    pq.finalize()
