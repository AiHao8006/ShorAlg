from pyqpanda import *

if __name__ == "__main__":
    init(QMachineType.CPU)
    qubits = qAlloc_many(3)
    cbits = cAlloc_many(3)
    qubit = qAlloc_many(1)
    prog = create_empty_qprog()

    # 构建量子程序
    prog << X(qubits[0]).dagger() \
    << Measure(qubits[0], cbits[0]) \
        # 对量子程序进行概率测量
    result = directly_run(prog)
    print(result)

    if result['c0']:
        print("qubit 1")
        prog << X(qubits[1]) << Reset(qubits[0])
    else:
        print("qubit 2")
        prog << X(qubits[2]) << Reset(qubits[0])
    prog << measure_all(qubits, cbits)
    result = directly_run(prog)
    print(result)

    prog << X(qubit) << Measure(qubit[0], cbits[0])
    result = directly_run(prog)
    print(result)

    # 打印测量结果

    finalize()
