from pyqpanda import *
import numpy as np


def CARRY(carry_qubits):
    Gate_set = create_empty_circuit()
    Gate_set << X(qubits[3]).control([qubits[1], qubits[2]]) \
             << X(qubits[2]).control(qubits[1]) \
             << X(qubits[3]).control([qubits[0], qubits[2]])
    return Gate_set


if __name__ == '__main__':
    init(QMachineType.CPU)
    qubits = qAlloc_many(5)

    prog = QProg()
    prog << X(qubits[0]) << X(qubits[1]) << CARRY([qubits[0], qubits[1], qubits[2], qubits[3]])

    results = prob_run_dict(prog, qubits, -1)

    print(results)
    finalize()

