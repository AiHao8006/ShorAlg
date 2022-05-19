import pyqpanda as pq
import numpy as np
from CompoundGates import CompoundGates

G = CompoundGates(n=4)

if __name__ == "__main__":

    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = pq.qAlloc_many(4)

    prog = pq.QProg()
    prog << pq.X(qubits[1]) << pq.X(qubits[0]) \
    << G.QFT(qubits) \
    << G.PhiADD(qubits, 7) \
    << G.QFT(qubits, inverse=True)

    result = pq.prob_run_dict(prog, qubits, -1)
    for key in result:
        print(key + " : " + str(result[key]))
    pq.finalize()
