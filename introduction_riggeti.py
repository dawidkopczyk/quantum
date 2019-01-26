from pyquil import Program, get_qc
from pyquil.api import WavefunctionSimulator

#==============================================================================
# Initilization
#==============================================================================
qc = get_qc('2q-qvm')
prog = Program()

#==============================================================================
# Qubit
#==============================================================================
from pyquil.gates import I
prog.inst(I(1), I(0))

# Print current quantum state of the system
state = WavefunctionSimulator().wavefunction(prog)
print("The system is in state: {}".format(state))

# Probabilities
print("Probability that after measurement the system is in state 00 {}".format(abs(state.amplitudes[0])**2))
print("Probability that after measurement the system is in state 01 {}".format(abs(state.amplitudes[1])**2))
print("Probability that after measurement the system is in state 10 {}".format(abs(state.amplitudes[2])**2))
print("Probability that after measurement the system is in state 11 {}".format(abs(state.amplitudes[3])**2))

#==============================================================================
# Quantum gates
#==============================================================================
from pyquil.gates import X
prog.inst(X(0))

# Print current quantum state of the system
state = WavefunctionSimulator().wavefunction(prog)
print("The system is in state: {}".format(state))

# Swap gate
from pyquil.gates import SWAP
prog.inst(SWAP(1, 0))

# Print current quantum state of the system
state = WavefunctionSimulator().wavefunction(prog)
print("The system is in state: {}".format(state))

# Hadamard gate
from pyquil.gates import H
prog.inst(H(1))

# Print current quantum state of the system
state = WavefunctionSimulator().wavefunction(prog)
print("The system is in state: {}".format(state))

#==============================================================================
# Measurment
#==============================================================================
# Classical regsitry storing the results
ro = prog.declare('ro', 'BIT', 2)
# Measure
prog.measure(1, ro[0])
prog.measure(0, ro[1])
# Compile and run
prog_exec = qc.compile(prog)
ret = qc.run(prog_exec)
print("The first qubit is in state |{}> and second in state |{}> after measurment".format(*ret[0]))

# Repeat the experiment 1000 times
prog.wrap_in_numshots_loop(1000)
# Compile and run
prog_exec = qc.compile(prog)
ret = qc.run(prog_exec)
freq_first_is_0 = [trial[0] for trial in ret].count(0) / 1000
freq_first_is_1 = [trial[0] for trial in ret].count(1) / 1000
freq_second_is_0 = [trial[1] for trial in ret].count(0) / 1000
print("Relative frequency of measuring the first qubit in |0> state: {}".format(freq_first_is_0))
print("Relative frequency of measuring the first qubit in |1> state: {}".format(freq_first_is_1))
print("Relative frequency of measuring the second qubit in |0> state: {}".format(freq_second_is_0))