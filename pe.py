import numpy as np
import math

from pyquil import Program, get_qc
from pyquil.gates import SWAP, H, CPHASE

# =============================================================================
# Create connection with QVM and initilize program
# =============================================================================
qc = get_qc('3q-qvm')
prog = Program()

# =============================================================================
# Inputs
# =============================================================================
U = np.array([[1j, 0],
              [0, -1j]])
phi = np.array([[1],
                [0]])

# =============================================================================
# Step 1. Initialization
# =============================================================================
n, m = 2, 1
control_qubits = range(n)
phi_qubits = range(n, n+m)
# Classical regsitry storing the results
ro = prog.declare('ro', 'BIT', len(control_qubits))

# =============================================================================
# Step 2. Create superposition
# =============================================================================
for i in control_qubits:
    # Apply Hadamard gate
    prog.inst(H(i))
    
# =============================================================================
# Step 3. Apply controlled unitary gates
# =============================================================================
def create_C_U(U):
    # The matrix representing the controlled U has a block form of 
    # [[eye,zeros],
    #  [zeros,U]]
    k = len(U)
    C_U = np.vstack([np.hstack([np.eye(k),       np.zeros((k,k))]), 
                     np.hstack([np.zeros((k,k)), U])])
    return C_U
    
for i in control_qubits:
    if i > 0:
        U = np.dot(U, U)
    # Define controlled unitary
    C_U = create_C_U(U)
    name = 'C_U-{0}'.format(2 ** i)
    prog.defgate(name, C_U)
    # Apply controlled unitary
    prog.inst((name, i) + tuple(phi_qubits))
    
# =============================================================================
# Step 4. Apply inverse quantum Fourier transform 
# =============================================================================
def inverse_qft_2q(qubits):
    
    prog = Program()
    
    prog += SWAP(0, 1)
    # QFT is unitary, thus the inverse QFT contains reversed order of gates 
    # with complex conjugate in CPHASE
    prog += H(0)
    prog += CPHASE(-math.pi / 2, 0, 1)
    prog += H(1)
    
    return prog

prog += inverse_qft_2q(control_qubits)

# =============================================================================
# Step 5. Measurement
# =============================================================================
for i in control_qubits:
    # Measure i-th control qubit and put output to classical bit
    prog.measure(i, ro[i])

# =============================================================================
# Step 6. Compile and execute
# =============================================================================
#prog.wrap_in_numshots_loop(10)
prog_exec = qc.compile(prog)
result = qc.run(prog_exec)
print(result)

#from pyquil.api import WavefunctionSimulator
#print(WavefunctionSimulator().wavefunction(prog)) 

