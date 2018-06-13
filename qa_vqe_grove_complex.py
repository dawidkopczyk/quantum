import numpy as np
from scipy.optimize import minimize

from pyquil.quil import Program
from pyquil.api import QVMConnection

# Define matrix
from pyquil.paulis import PauliSum, PauliTerm
H = PauliSum([PauliTerm.from_list([("X", 2), ("Z", 1),("X", 0)], coefficient=0.2),
              PauliTerm.from_list([("X", 2), ("I", 1),("X", 0)], coefficient=0.9),
              PauliTerm.from_list([("Z", 2), ("Z", 1),("Z", 0)], coefficient=0.3)])

# Define ansatz
n_qubits, depth = 3, 3
from pyquil.gates import RY, CNOT
def ansatz(params):
    p = Program()
    for i in range(depth):
        p += CNOT(2,0)
        for j in range(n_qubits):
            p += Program(RY(params[j], j))
    return p

# Minimize and get approximate of the lowest eigenvalue
from grove.pyvqe.vqe import VQE
qvm = QVMConnection()
vqe = VQE(minimizer=minimize, minimizer_kwargs={'method': 'nelder-mead', 
                                                'options': {'xatol': 1.0e-2}})

np.random.seed(999)
initial_params = np.random.uniform(0.0, 2*np.pi, size=n_qubits)
result = vqe.vqe_run(ansatz, H, initial_params, samples=None, qvm=qvm)
print(result)