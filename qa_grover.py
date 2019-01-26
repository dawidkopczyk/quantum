import numpy as np

from pyquil import Program, get_qc
from pyquil.gates import H, I
from pyquil.api import WavefunctionSimulator

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
qc = get_qc('9q-square-qvm')
gr_prog = Program()
        
# \psi_0: Qubits initilization
qubits = list(reversed(range(N)))
gr_prog.inst([I(q) for q in qubits])
#print(WavefunctionSimulator().wavefunction(gr_prog))

# \psi_1: Apply Hadamard gates
gr_prog.inst([H(q) for q in qubits])
#print(WavefunctionSimulator().wavefunction(gr_prog))

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
    #print(WavefunctionSimulator().wavefunction(gr_prog))
    
    # \psi_3^i:  Apply Inversion around the mean
    gr_prog.inst(tuple([DIFFUSION_GATE_NAME] + qubits))
    #print(WavefunctionSimulator().wavefunction(gr_prog))

# \psi_5: Measure
ro = gr_prog.declare('ro', 'BIT', N) # Classical registry storing the results
for q in qubits:
    gr_prog.measure(q, ro[q])

# Compile and run
prog_exec = qc.compile(gr_prog)
ret = qc.run(prog_exec)
ret_string = ''.join([str(q) for q in reversed(ret[0])])
print("The searched string is: {}".format(ret_string))
