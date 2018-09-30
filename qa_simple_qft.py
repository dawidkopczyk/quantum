#==============================================================================
# DFT
#==============================================================================
import numpy as np
x = np.array([0.5, 0.5, 0.5, 0.5])
y = np.fft.fft(x, norm='ortho')
print(y)

x = np.fft.ifft(y, norm='ortho')
print(x)

#==============================================================================
# QFT
#==============================================================================
import math
from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.gates import SWAP, H, CPHASE

# Create connection with QVM and initilize program
qvm = QVMConnection()
prog = Program()

# Prepare state
prog = prog.inst(H(0),H(1))
print('Amplitudes a of input state psi: {}'.format(qvm.wavefunction(prog).amplitudes))

# Perfrom QFT
prog += SWAP(0, 1)
prog += H(1)
prog += CPHASE(math.pi / 2, 0, 1)
prog += H(0)

print('Amplitudes b of output state phi: {}'.format(qvm.wavefunction(prog).amplitudes))





