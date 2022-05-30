import pyqpanda as pq
import numpy as np
from CompoundGates_Reset import CompoundGates

G = CompoundGates(n=5)

pq.init(pq.QMachineType.CPU)
qubits = pq.qAlloc_many(6)

qubits_x = [qubits[i] for i in range(5)]
qubit_aux = qubits[5]

prog = pq.create_empty_qprog()

prog << pq.X(qubits_x[1]) << pq.X(qubits_x[2])
prog << G.QFT(qubits_x, n=5)
prog = G.PhiADD_MOD(prog, qubits_x, qubit_aux, 11, 15)
prog << G.QFT(qubits_x, n=5, inverse=True)

prog << G.QFT(qubits_x, n=5)
prog = G.PhiADD_MOD(prog, qubits_x, qubit_aux, 3, 15)
prog << G.QFT(qubits_x, n=5, inverse=True)

prog << G.QFT(qubits_x, n=5)
prog = G.PhiADD_MOD(prog, qubits_x, qubit_aux, 6, 15, inverse=True)
prog << G.QFT(qubits_x, n=5, inverse=True)

result = pq.prob_run_dict(prog, qubits_x, -1)
i = 0
for key in result:
    print(i, key + " : " + str(result[key]))
    i = i + 1
print('\n')
