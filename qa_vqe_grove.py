from scipy.optimize import minimize

from pyquil.quil import Program
from pyquil.api import QVMConnection

import numpy as np

# Define matrix
from pyquil.paulis import PauliSum, PauliTerm
H = PauliSum([PauliTerm.from_list([("X", 2), ("Z", 1),("X", 0)], coefficient=0.2),
              PauliTerm.from_list([("X", 2), ("I", 1),("X", 0)], coefficient=0.9),
              PauliTerm.from_list([("Z", 2), ("Z", 1),("Z", 0)], coefficient=0.3)])

# Define ansatz
from pyquil.gates import RY, X
def ansatz(params):
    p = Program(RY(params[0], 0), RY(params[1], 1), RY(params[2], 2))
    gate_num = int(np.round(params[3]))
    for gate in range(gate_num):
        p.inst(X(1))
    return p

# Minimize and get approximate of the lowest eigenvalue
from grove.pyvqe.vqe import VQE
qvm = QVMConnection()
vqe = VQE(minimizer=minimize, minimizer_kwargs={'method': 'nelder-mead'})

initial_params = [1.0, 1.0, 1.0, 5]
result = vqe.vqe_run(ansatz, H, initial_params, samples=None, qvm=qvm)
print(result)