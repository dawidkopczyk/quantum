import numpy as np
from pyquil.quil import Program
from pyquil.api import QVMConnection

#==============================================================================
# Initilization
#==============================================================================
qvm = QVMConnection()
prog = Program()

#==============================================================================
# Qubit
#==============================================================================
from pyquil.gates import I
prog.inst(I(1), I(0))

# Print current quantum state of the system
state = qvm.wavefunction(prog)
print("The system is in state: {}".format(state))

# Probabilities
print("Probability that after measurement the system is in state 00 {}".format(abs(state.amplitudes[0])**2))
print("Probability that after measurement the system is in state 01 {}".format(abs(state.amplitudes[1])**2))
print("Probability that after measurement the system is in state 10 {}".format(abs(state.amplitudes[2])**2))
print("Probability that after measurement the system is in state 11 {}".format(abs(state.amplitudes[3])**2))

#==============================================================================
# Quantum gates
#==============================================================================
from pyquil.gates import X
prog.inst(X(0))

# Print current quantum state of the system
state = qvm.wavefunction(prog)
print("The system is in state: {}".format(state))

# Optional: use list in decreasing order as qubit indices
qubits = [1, 0]

# Swap gate
from pyquil.gates import SWAP
prog.inst(SWAP(1, 0))

# Print current quantum state of the system
state = qvm.wavefunction(prog)
print("The system is in state: {}".format(state))

# Optional: use list in decreasing order as qubit indices
prog.inst(SWAP(qubits[0], qubits[1]))

# Hadamard gate
from pyquil.gates import H
prog.inst(H(1))

# Print current quantum state of the system
state = qvm.wavefunction(prog)
print("The system is in state: {}".format(state))

#==============================================================================
# Measurment
#==============================================================================
prog.measure(qubit_index=1, classical_reg=0)
prog.measure(qubit_index=0, classical_reg=1)

ret = qvm.run(prog, classical_addresses=[0, 1])
print("The first qubit is in state |{}> and second in state |{}> after measurment".format(*ret[0]))

ret = qvm.run(prog, classical_addresses=[0, 1], trials=1000)
freq_first_is_0 = [trial[0] for trial in ret].count(0) / 1000
freq_first_is_1 = [trial[0] for trial in ret].count(1) / 1000
freq_second_is_1 = [trial[1] for trial in ret].count(1) / 1000
print("Relative frequency of measuring the first qubit in |0> state: {}".format(freq_first_is_0))
print("Relative frequency of measuring the first qubit in |0> state: {}".format(freq_first_is_1))
print("Relative frequency of measuring the second qubit in |1> state: {}".format(freq_second_is_1))