from pyquil.api import QVMConnection
from grove.deutsch_jozsa.deutsch_jozsa import DeutschJosza

# Connection
qvm = QVMConnection()

#==============================================================================
# Grove: Deutsch-Jozsa Algorithm
#==============================================================================
# Define a balanced function
mapping = {'000': '1', '001': '1', '010': '1', '011': '1',
           '100': '0', '101': '0', '110': '0', '111': '0'}

# Run
algo = DeutschJosza()
ret = algo.is_constant(qvm, bitstring_map=mapping)    
if ret:
    print("The function is constant")
else:
    print("The function is balanced")