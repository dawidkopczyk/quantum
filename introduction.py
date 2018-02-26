import numpy as np

# Create zero and one states
state_zero = np.array([[1.0],
                       [0.0]])
state_one = np.array([[0.0],
                      [1.0]])

# Superposition
c1 = 1.0 / 2**0.5
c2 = 1.0 / 2**0.5
state_super = c1 * state_zero + c2 * state_one
print(state_super)

# Assembling qunatum states
state_three = np.kron(np.kron(state_zero, state_one), state_one)
print(state_three)

def multi_kron(*args):
    ret = np.array([[1.0]])
    for q in args:
        ret = np.kron(ret, q)
    return ret

state_multi = multi_kron(state_zero, state_one, state_one, 
                         state_one, state_zero, state_one)

print(state_multi)
print(state_multi.shape)

# Qunatum gates
gate_H = 1.0 / 2**0.5 * np.array([[1, 1],
                             [1, -1]])
    
state_new = np.dot(gate_H, state_zero)
print(state_new)

gate_SWAP = np.array([[1,0,0,0],
                      [0,0,1,0],
                      [0,1,0,0],
                      [0,0,0,1]])
    
state_t0 = multi_kron(state_zero, state_one)
state_t1 = np.dot(gate_SWAP, state_t0)
print(state_t1)

gate_I = np.eye(2)
state_t0 = multi_kron(state_zero, state_one)
state_t1 = np.dot(multi_kron(gate_H, gate_I), state_t0)
print(state_t1)

# Prepare state
state = np.dot(multi_kron(gate_H, gate_H), multi_kron(state_zero, state_zero))

# Projectors
P0 = np.dot(state_zero, state_zero.T)
P1 = np.dot(state_one, state_one.T)

# Probability of first qubit being in state 0
rho = np.dot(state, state.T)
prob0 = np.trace(np.dot(multi_kron(P0, gate_I), rho))

# Simulate
if np.random.rand() < prob0:
    ret = 0
    state_ret = np.dot(multi_kron(P0, gate_I), state)
else:
    ret = 1
    state_ret = np.dot(multi_kron(P1, gate_I), state) 
    
# Normalize
from scipy import linalg
state_ret /= linalg.norm(state_ret)

print("Qubit Measured: \n {} \n After-Measurment State: \n {}".format(ret, state_ret))

