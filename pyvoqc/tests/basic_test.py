# Run all supported functions to check for obvious errors (e.g. seg faults)

from pyvoqc.voqc import VOQCCircuit, get_library_handle
import os

rel = os.path.dirname(os.path.abspath(__file__))

lib = get_library_handle()

c = VOQCCircuit(lib, os.path.join(rel,"../../tutorial-files/tof_3_example.qasm"))
c.write("out.qasm")
os.remove("out.qasm")
c.count_gates()
c.count_rzq_clifford()
c.total_gate_count()
c.check_well_typed(5)
c.convert_to_rzq()
c.convert_to_ibm()
c.decompose_to_cnot()
c.replace_rzq()
c.optimize_ibm()
c.not_propagation()
c.hadamard_reduction()
c.cancel_single_qubit_gates()
c.cancel_two_qubit_gates()
c.merge_rotations()
c.optimize_nam()
c.optimize()
c.trivial_layout(5)
c.list_to_layout([2,0,1,3,4])
c.c_graph_from_coupling_map(5, [(1, 0), (2, 0), (2, 1), (3, 2), (3, 4), (4, 2)])
c.decompose_swaps()
c.check_constraints()
c2 = VOQCCircuit(lib, os.path.join(rel,"../../tutorial-files/tof_3_example.qasm"))
c2.trivial_layout(5)
c.check_swap_equivalence(c2)

# If you get here, then nothing crashed.
print("Basic tests passed.")