import pyqpanda as pq

if __name__ == "__main__":

    pq.init(pq.QMachineType.CPU)
    qubits = pq.qAlloc_many(4)
    cbits = pq.cAlloc_many(4)

    # 构建量子程序
    prog = pq.QProg()
    circuit = pq.create_empty_circuit()

    circuit << pq.H(qubits[0]) \
            << pq.CNOT(qubits[0], qubits[1]) \
            << pq.CNOT(qubits[1], qubits[2]) \

    prog << circuit << pq.Measure(qubits[0], cbits[0])


    # 量子程序运行1000次，并返回测量结果
    result = pq.run_with_configuration(prog, cbits, 1000)

    # 打印量子态在量子程序多次运行结果中出现的次数
    print(result)
    pq.finalize()