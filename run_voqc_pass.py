from qiskit import QuantumCircuit
from qiskit.test.mock import FakeAlmaden
from qiskit.transpiler import CouplingMap
from pyvoqc.qiskit import voqc_pass_manager

backend = FakeAlmaden() # has 20 qubits
coupling_map = CouplingMap(couplinglist=backend.configuration().coupling_map)

# Default optimization (= "optimize") followed by default Qiskit
# layout and routing (= "sabre"). See pyvoqc/qiskit/voqc_pass.py for more options.
vpm = voqc_pass_manager(coupling_map=coupling_map)

circ = QuantumCircuit.from_qasm_file("pyvoqc/tests/test_qasm_files/tof_10.qasm") # has 19 qubits
print("Input circuit stats:", circ.count_ops())

new_circ = vpm.run(circ)
print("Output circuit stats:", new_circ.count_ops())