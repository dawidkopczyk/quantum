import numpy as np
from scipy import linalg

#==============================================================================
# Quantum Computation objects
#==============================================================================
state_zero = np.array([[1.0],
                       [0.0]])
state_one = np.array([[0.0],
                      [1.0]])

# Multi Kron
def multi_kron(*args):
    ret = np.array([[1.0]])
    for q in args:
        ret = np.kron(ret, q)
    return ret

# Gates
gate_I = np.eye(2)
    
# Projectors
P0 = np.dot(state_zero, state_zero.T)
P1 = np.dot(state_one, state_one.T)

#==============================================================================
# Quantum Entanglement
#==============================================================================
#Initilize states straigtaway
psi = 0.5 * (multi_kron(state_zero, state_zero) + multi_kron(state_zero, state_one) +
             multi_kron(state_one, state_zero) + multi_kron(state_one, state_one))
phi = 1.0 / 2**0.5 * (multi_kron(state_zero, state_one) +  multi_kron(state_one, state_zero))

# Optional ====================================================================
# Initilize states from scratch
gate_X = np.array([[0, 1],
                   [1, 0]])
gate_H = 1.0 / 2**0.5 * np.array([[1, 1],
                                  [1, -1]])
gate_CNOT = np.array([[1,0,0,0],
                      [0,1,0,0],
                      [0,0,0,1],
                      [0,0,1,0]])
psi = np.dot(multi_kron(gate_H, gate_H), multi_kron(state_zero, state_zero))
phi = np.dot(gate_CNOT, np.dot(multi_kron(gate_H, gate_X), multi_kron(state_zero, state_zero)))
#==============================================================================

print(psi)
print(phi)

# Function measuring both qubits
def measure_two(state):
    # Probability of first qubit being in state 0
    rho_1 = np.dot(state, state.T)
    prob0_1 = np.trace(np.dot(multi_kron(P0, gate_I), rho_1))
    
    # Simulate
    if np.random.rand() < prob0_1:
        ret = '0'
        state_ret_1 = np.dot(multi_kron(P0, gate_I), state)
    else:
        ret = '1'
        state_ret_1 = np.dot(multi_kron(P1, gate_I), state) 
        
    # Normalize
    state_ret_1 /= linalg.norm(state_ret_1)
    
    # Probability of second qubit being in state 0
    rho_2 = np.dot(state_ret_1, state_ret_1.T)
    prob0_2 = np.trace(np.dot(multi_kron(gate_I, P0), rho_2))
    
    # Simulate
    if np.random.rand() < prob0_2:
        ret += '0'
        state_ret_2 = np.dot(multi_kron(gate_I, P0), state_ret_1)
    else:
        ret += '1'
        state_ret_2 = np.dot(multi_kron(gate_I, P1), state_ret_1) 
        
    # Normalize
    state_ret_2 /= linalg.norm(state_ret_2)
    
    return ret, state_ret_2
  
# Measure both qubits in psi
ret, state_ret = measure_two(psi)                   
print("Qubit Measured: \n {} \n After-Measurment State: \n {}".format(ret, state_ret))

# See probabilities
acc = []
for i in range(10**4):
    _, state_ret = measure_two(psi)
    acc.append(state_ret)
prob = np.array(acc).mean(axis=0).ravel()
print('Empirical probabilities 00, 01, 10, 11: {}'.format(prob))

# Measure both qubits in psi
ret, state_ret = measure_two(phi)                   
print("Qubit Measured: \n {} \n After-Measurment State: \n {}".format(ret, state_ret))

# See probabilities
acc = []
for i in range(10**4):
    _, state_ret = measure_two(phi)
    acc.append(state_ret)
prob = np.array(acc).mean(axis=0).ravel()
print('Empirical probabilities 00, 01, 10, 11: {}'.format(prob))