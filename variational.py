import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=1)

@qml.qnode(dev)
def circuit(params):
    qml.RY(params[0], wires=0)
    return qml.expval.PauliZ(0)

print('The expectation value {}'.format(circuit([0])))
print('The expectation value {}'.format(circuit([np.pi/3])))
print('The expectation value {}'.format(circuit([np.pi])))

def objective(var):
    return circuit(var)

np.random.seed(2019)
initial_theta = 2*np.pi*np.random.random_sample()
init_params = np.array([initial_theta])
print('Initial objective function value {:.7f} for theta={:.2f}'.format(objective(init_params),
                                                                        initial_theta))
# Initilize Gradient Descent Optimizer
opt = qml.GradientDescentOptimizer(stepsize=0.4)

# set the number of steps
steps = 30
# set the initial parameter values
params = init_params

for i in range(steps):
    # update the circuit parameters
    params = opt.step(objective, params)
    print('Cost after step {:5d}: {: .7f}'.format(i+1, objective(params)))

print('Optimized rotation angle: {}'.format(params))