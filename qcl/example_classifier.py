#==============================================================================
# Generate data and labels
#==============================================================================
import numpy as np
from sklearn.datasets import make_circles
np.random.seed(0)
m = 10
X, y = make_circles(n_samples=m, factor=.1, noise=.0, random_state=0)


#==============================================================================
# Programs
#==============================================================================   
from qcl import (ising_prog_gen, default_input_state_gen, 
                 default_output_state_gen, default_grad_state_gen)

n_qubits, depth = 4, 4

ising_prog = ising_prog_gen(trotter_steps=1000, T=10, n_qubits=n_qubits)
state_generators = dict()
state_generators['input'] = default_input_state_gen(n_qubits)
state_generators['output'] = default_output_state_gen(ising_prog, n_qubits, depth)
state_generators['grad'] = default_grad_state_gen(ising_prog, n_qubits, depth)

#==============================================================================
# Quantum Circuit Learning - Classification 
#==============================================================================
import qsimulator as pq
from qsimulator import Z
from qcl import QCL

initial_theta = np.random.uniform(0.0, 2*np.pi, size=3*n_qubits*depth)

operator1 = pq.Program(n_qubits)
operator1.inst(Z, 0)
operator2 = pq.Program(n_qubits)
operator2.inst(Z, 1)
operator_programs = [operator1, operator2] 

est = QCL(state_generators, initial_theta, loss="binary_crossentropy",  
          operator_programs=operator_programs, epochs=20, batch_size=m,
          verbose=True)

est.fit(X,y)
results = est.get_results()

#==============================================================================
# PLots
#==============================================================================
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
cm = plt.cm.RdBu
cm_bright = ListedColormap(['#FF0000', '#0000FF'])
xx, yy = np.meshgrid(np.linspace(-1.0, 1.0, 10),
                     np.linspace(-1.0, 1.0, 10))
y_pred = est.predict(np.c_[xx.ravel(), yy.ravel()])[:,0]
Z = y_pred.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap=cm, alpha=.8)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cm_bright, edgecolors='k')