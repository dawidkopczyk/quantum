import numpy as np

from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.gates import H, I

#==============================================================================
# Construct quantum oracle (not a part of algorithm)
#==============================================================================
SEARCHED_STRING = "10"
N = len(SEARCHED_STRING)
oracle = np.zeros(shape=(2 ** N, 2 ** N))
for b in range(2 ** N):
    if np.binary_repr(b, N) == SEARCHED_STRING:
        oracle[b, b] = -1
    else:
        oracle[b, b] = 1
print(oracle)

#==============================================================================
# Grover's Search Algorithm
#==============================================================================
qvm = QVMConnection()
gr_prog = Program()
        
# \psi_0: Qubits initilization
qubits = list(reversed(range(N)))
gr_prog.inst([I(q) for q in qubits])
#print(qvm.wavefunction(gr_prog))

# \psi_1: Apply Hadamard gates
gr_prog.inst([H(q) for q in qubits])
#print(qvm.wavefunction(gr_prog))

# Define quantum oracle
ORACLE_GATE_NAME = "GROVER_ORACLE"
gr_prog.defgate(ORACLE_GATE_NAME, oracle)

# Define inversion around the mean
DIFFUSION_GATE_NAME = "DIFFUSION"
diffusion = 2.0 * np.full((2**N, 2**N), 1/(2**N)) - np.eye(2**N)
gr_prog.defgate(DIFFUSION_GATE_NAME, diffusion)

# Number of algorithm iterations
N_ITER = int(np.pi / 4 * np.sqrt(2**N))

# Loop
for i in range(N_ITER):
    
    # \psi_2^i:  Apply Quantum Oracle
    gr_prog.inst(tuple([ORACLE_GATE_NAME] + qubits))
    #print(qvm.wavefunction(gr_prog))
    
    # \psi_3^i:  Apply Inversion around the mean
    gr_prog.inst(tuple([DIFFUSION_GATE_NAME] + qubits))
    #print(qvm.wavefunction(gr_prog))

# \psi_5: Measure
for q in qubits:
    gr_prog.measure(qubit_index=q, classical_reg=q)

# Run
ret = qvm.run(gr_prog, classical_addresses=qubits)
ret_string = ''.join([str(q) for q in ret[0]])
print("The searched string is: {}".format(ret_string))
