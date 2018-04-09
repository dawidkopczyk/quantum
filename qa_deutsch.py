import numpy as np

from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.gates import X, H, I

#==============================================================================
# Deutsch Algorithm
#==============================================================================
qvm = QVMConnection()
d_prog = Program()

# \psi_0: Qubit initilization
qubits = [1, 0]
d_prog.inst(I(qubits[0]), I(qubits[1]))
#print(qvm.wavefunction(d_prog))

# \psi_1: Put ancilla qubit into 1
d_prog.inst(X(qubits[1]))
#print(qvm.wavefunction(d_prog))

# \psi_2: Apply Hadamard gates
d_prog.inst(H(qubits[0]), H(qubits[1]))
#print(qvm.wavefunction(d_prog))

# \psi_3:  Apply Quantum Oracle
# Quantum oracle
ORACLE_GATE_NAME = "DEUTSCH_JOZSA_ORACLE"
oracle = np.array([[0,1,0,0],
                   [1,0,0,0],
                   [0,0,0,1],
                   [0,0,1,0]])
d_prog.defgate(ORACLE_GATE_NAME, oracle)
d_prog.inst((ORACLE_GATE_NAME, qubits[0], qubits[1]))
#print(qvm.wavefunction(d_prog))

# \psi_4: Apply Hadamard gate
d_prog.inst(H(qubits[0]))
#print(qvm.wavefunction(d_prog))

# \psi_5: Measure
d_prog.measure(qubit_index=qubits[0], classical_reg=0)

# Run
ret = qvm.run(d_prog, classical_addresses=[0])
if ret[0][0] == 0:
    print("The function is constant")
else:
    print("The function is balanced")