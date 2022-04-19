from qiskit import QuantumCircuit
from qiskit.qasm import pi
from qiskit.test.mock import FakeAlmaden
from qiskit.transpiler import CouplingMap
from qiskit.transpiler import PassManager

from pyvoqc.voqc import VOQCError
from pyvoqc.qiskit import voqc_pass_manager

import os
import unittest

rel = os.path.dirname(os.path.abspath(__file__))

class TestQiskitPass(unittest.TestCase):

    def test_tof_10(self):
        before = QuantumCircuit.from_qasm_file(os.path.join(rel, "test_qasm_files/tof_10.qasm"))
        after = QuantumCircuit.from_qasm_file(os.path.join(rel, "test_qasm_files/optim_tof_10.qasm"))
        self.assertEqual(self.run_optimization(before, ["optimize_nam"]), after)

    def test_not_propagation(self):
        before = QuantumCircuit(2)
        before.x(1)
        before.cx(0, 1)
        after = QuantumCircuit(2)
        after.cx(0, 1)
        after.x(1)
        self.assertEqual(self.run_optimization(before, ["optimize_nam"]), after)

    def test_cancel_single_qubit_gates(self):
        before = QuantumCircuit(1)
        before.rz(pi/2, 0)
        before.h(0)
        before.h(0)
        after = QuantumCircuit(1)
        after.s(0)
        self.assertEqual(self.run_optimization(before, ["cancel_single_qubit_gates"]), after)

    def test_cancel_two_qubit_gates(self):
        before = QuantumCircuit(2)
        before.cx(0, 1)
        before.cx(0, 1)
        before.h(0)
        after = QuantumCircuit(2)
        after.h(0)
        self.assertEqual(self.run_optimization(before, ["cancel_two_qubit_gates"]), after)

    def test_merge_rotations(self):
        before = QuantumCircuit(1)
        before.rz(pi/4, 0)
        before.rz(pi/4, 0)
        after = QuantumCircuit(1)
        after.s(0)
        self.assertEqual(self.run_optimization(before, ["merge_rotations"]), after)

    def test_hadamard_reduction(self):
        before = QuantumCircuit(1)
        before.h(0)
        before.rz(pi/2, 0)
        before.h(0)
        after = QuantumCircuit(1)
        after.sdg(0)
        after.h(0)
        after.sdg(0)
        self.assertEqual(self.run_optimization(before, ["hadamard_reduction"]), after)

    def test_invalid_function(self):
        before = QuantumCircuit(1)
        before.x(0)
        with self.assertRaises(VOQCError):
            self.run_optimization(before, ["foo"])
            
    def test_invalid_gate(self):
        before = QuantumCircuit(2)
        before.ch(0,1)
        with self.assertRaises(VOQCError):
            self.run_optimization(before)
    
    def test_trivial_basic_passes_validation(self):
        c = QuantumCircuit.from_qasm_file(os.path.join(rel, "test_qasm_files/tof_10.qasm"))
        self.run_mapping(c, "trivial", "basic")

    def test_dense_stochastic_passes_validation(self):
        c = QuantumCircuit.from_qasm_file(os.path.join(rel, "test_qasm_files/tof_10.qasm"))
        self.run_mapping(c, "dense", "stochastic")

    def test_noise_lookahead_passes_validation(self):
        c = QuantumCircuit.from_qasm_file(os.path.join(rel, "test_qasm_files/tof_10.qasm"))
        self.run_mapping(c, "noise_adaptive", "lookahead")

    def test_sabre_sabre_passes_validation(self):
        c = QuantumCircuit.from_qasm_file(os.path.join(rel, "test_qasm_files/tof_10.qasm"))
        self.run_mapping(c, "sabre", "sabre")

    def run_optimization(self, circ, opts=None):
        vpm = voqc_pass_manager(post_opts=opts)
        new_circ = vpm.run(circ)
        return new_circ

    def run_mapping(self, circ, layout, routing):
        backend = FakeAlmaden()
        c_map = CouplingMap(couplinglist=backend.configuration().coupling_map)
        props = backend.properties()
        vpm = voqc_pass_manager(post_opts=[], layout_method=layout, routing_method=routing, backend_properties=props, coupling_map=c_map)
        new_circ = vpm.run(circ)
        return new_circ

if __name__ == "__main__":
    unittest.main()
