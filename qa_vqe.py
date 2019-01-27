import numpy as np
from scipy.optimize import minimize

from pyquil import Program, get_qc

#==============================================================================
# Variational-Quantum-Eigensolver
#==============================================================================
# Create connection with QVM
qc = get_qc('2q-qvm')

# Define matrix
from pyquil.paulis import sZ
H = sZ(0)

# Define ansatz
from pyquil.gates import RY
def ansatz(params):
    return Program(RY(params[0], 0))

# Function calculating expectation value
def expectation(params):
    
    # Define number of measurments
    samples = 10000
    
    # Define program
    prog = ansatz(params)
    
    # Measure
    ro = prog.declare('ro', 'BIT', 1) # Classical registry storing the results
    prog.measure(0, ro[0])
    
    # Compile and execute
    prog.wrap_in_numshots_loop(samples)
    prog_exec = qc.compile(prog)
    ret = qc.run(prog_exec)
    
    # Calculate expectation
    freq_is_0 = [trial[0] for trial in ret].count(0) / samples
    freq_is_1 = [trial[0] for trial in ret].count(1) / samples
    
    return freq_is_0 - freq_is_1

# Test of expectation value function  
test = expectation([0.0]) 
print(test)

# Draw expectation alue against parameter value
params_range = np.linspace(0.0, 2 * np.pi, 25)
data = [expectation([params]) for params in params_range]

import matplotlib.pyplot as plt
plt.xlabel('Parameter value')
plt.ylabel('Expectation value')
plt.plot(params_range, data)
plt.show()

# Minimize and get approximate of the lowest eigenvalue
initial_params = [0.0]
minimum = minimize(expectation, initial_params, method='Nelder-Mead', 
                   options={'initial_simplex': np.array([[0.0], [0.05]]), 'xatol': 1.0e-2})
print(minimum)