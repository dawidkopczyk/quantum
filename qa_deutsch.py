import numpy as np

from pyquil import Program, get_qc
from pyquil.gates import X, H, I
from pyquil.api import WavefunctionSimulator

#==============================================================================
# Deutsch Algorithm
#==============================================================================
qc = get_qc('9q-square-qvm')
d_prog = Program()

# \psi_0: Qubit initilization
qubits = [1, 0]
d_prog.inst(I(qubits[0]), I(qubits[1]))
#print(WavefunctionSimulator().wavefunction(d_prog))

# \psi_1: Put ancilla qubit into 1
d_prog.inst(X(qubits[1]))
#print(WavefunctionSimulator().wavefunction(d_prog))

# \psi_2: Apply Hadamard gates
d_prog.inst(H(qubits[0]), H(qubits[1]))
#print(WavefunctionSimulator().wavefunction(d_prog))

# \psi_3:  Apply Quantum Oracle
# Quantum oracle
ORACLE_GATE_NAME = "DEUTSCH_JOZSA_ORACLE"
oracle = np.array([[0,1,0,0],
                   [1,0,0,0],
                   [0,0,0,1],
                   [0,0,1,0]])
d_prog.defgate(ORACLE_GATE_NAME, oracle)
d_prog.inst((ORACLE_GATE_NAME, qubits[0], qubits[1]))
#print(WavefunctionSimulator().wavefunction(d_prog))

# \psi_4: Apply Hadamard gate
d_prog.inst(H(qubits[0]))
#print(WavefunctionSimulator().wavefunction(d_prog))

# \psi_5: Measure
ro = d_prog.declare('ro', 'BIT', 1) # Classical registry storing the results
d_prog.measure(qubits[0], ro[0])

# Compile and run
prog_exec = qc.compile(d_prog)
ret = qc.run(prog_exec)
if ret[0][0] == 0:
    print("The function is constant")
else:
    print("The function is balanced")