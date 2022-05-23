import pyqpanda as pq
import numpy as np
from CompoundGates import CompoundGates

G = CompoundGates(n=4)

pq.init(pq.QMachineType.CPU)

qubits = pq.qAlloc_many(2 * G.n + 3)

qubits_x = [qubits[p] for p in range(0, G.n)]
qubits_0 = [qubits[p] for p in range(G.n, 2 * G.n + 1)]
qubit_measure = qubits[2 * G.n + 1]
qubit_aux = qubits[2 * G.n + 2]

cbits_x = pq.cAlloc_many(G.n)
cbits_0 = pq.cAlloc_many(G.n+1)
cbit_measure = pq.cAlloc_many(1)
cbit_aux = pq.cAlloc_many(1)

prog = pq.create_empty_qprog()

prog << pq.X(qubits_x[0])

# prog << pq.X(qubit_measure)
# prog << G.CU(qubit_measure, qubits_x, qubits_0, qubit_aux, 1, 15)     # control取0时，没有保持x为1
prog << G.C_MULT_MOD(qubit_measure, qubits_x, qubits_0, qubit_aux, 1, 15)   # X
# prog << G.PhiADD_MOD(qubits_x, qubit_aux, 0, 15, control_qubits=qubit_measure)  # X
prog << pq.H(qubit_measure)

prog << pq.measure_all(qubits_x, cbits_x)
result = pq.run_with_configuration(prog, cbits_x, 100)

print(result)
pq.finalize()
