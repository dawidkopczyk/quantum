import numpy as np
from grove.amplification.grover import Grover
from pyquil.api import QVMConnection

# Bitstring Map as an algorithm input
SEARCHED_STRING = "1011010"
N = len(SEARCHED_STRING)
mapping = {}
for b in range(2 ** N):
    pad_str = np.binary_repr(b, N)
    if pad_str == SEARCHED_STRING:
        mapping[pad_str] = -1
    else:
        mapping[pad_str] = 1

# Connection
qvm = QVMConnection()

#==============================================================================
# Grove: Grove's Search Algorithm
#==============================================================================
# Run
algo = Grover()
ret_string = algo.find_bitstring(qvm, bitstring_map=mapping)    
print("The searched string is: {}".format(ret_string))