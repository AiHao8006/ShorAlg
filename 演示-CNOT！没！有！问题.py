import pyqpanda as pq

pq.init(pq.QMachineType.CPU)

qubits = pq.qAlloc_many(2)
cbit = pq.cAlloc_many(1)

prog = pq.create_empty_qprog()
prog << pq.H(qubits[0])
# prog << pq.CNOT(qubits[0], qubits[1])
# prog << pq.CR(qubits[0], qubits[1], 0.1)
prog << pq.I(qubits[1]).control(qubits[0])
prog << pq.H(qubits[0])
prog << pq.Measure(qubits[0], cbit[0])

result = pq.run_with_configuration(prog, cbit, 100)
print(result)
pq.finalize()
