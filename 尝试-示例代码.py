from pyqpanda import *

if __name__ == "__main__":
   init(QMachineType.CPU)
   qubits = qAlloc_many(3)
   cbits = cAlloc_many(1)
   prog = create_empty_qprog()

   # 构建量子程序
   prog  << H(qubits) \
         << H(qubits[0]).dagger() \
         << X(qubits[2]).control([qubits[0], qubits[1]]) \
         << measure_all([1], [1])

   # 对量子程序进行概率测量
   result = directly_run(prog)

   # 打印测量结果
   print(result)
   finalize()