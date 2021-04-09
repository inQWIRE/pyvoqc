from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.transpiler.passes import Unroller
from qiskit import QuantumCircuit
from qiskit.transpiler.passes.basis import BasisTranslator
from qiskit.transpiler import PassManager
from pyvoqc.voqc import VOQC
from pyvoqc.exceptions import InvalidVOQCFunction, InvalidVOQCGate
from qiskit.transpiler.exceptions import TranspilerError
import os

class QiskitVOQC(TransformationPass):
    def __init__(self, funcs = None):
        
        super().__init__()
        self.voqc_functions = [
            "convert_to_rzq",
            "convert_to_ibm",
            "decompose_to_cnot", 
            "replace_rzq",
            "optimize_1q_gates",
            "cx_cancellation",
            "optimize_ibm",
            "not_propagation",
            "hadamard_reduction",
            "cancel_single_qubit_gates",
            "cancel_two_qubit_gates",
            "merge_rotations",
            "optimize_nam",
            "simple_map" ]
        self.voqc_gates = ['i', 'x', 'y', 'z', 'h', 's', 't', 'sdg', 'tdg', 'rx', 'ry', 
                           'rz', 'rzq', 'u1', 'u2', 'u3', 'cx', 'cz', 'swap', 'ccx', 'ccz']
        self.funcs = funcs if funcs else ["optimize_nam", "optimize_ibm"] # default optimization
        
        for i in range(len(self.funcs)):
            if not (self.funcs[i] in self.voqc_functions):
                raise InvalidVOQCFunction(str(self.funcs[i]), self.voqc_functions)
            
    def run(self, dag):
        
        # check if gates are supported in VOQC
        for node in dag.op_nodes():
            if not (node.name in self.voqc_gates):
                raise InvalidVOQCGate(node.name)

        # write qasm file 
        # TODO : would be nice if we could convert directly from Qiskit's circuit
        #        (requires support in OCaml code)
        circ = dag_to_circuit(dag)     
        circ.qasm(formatted=False, filename="temp_in.qasm")
        
        # apply VOQC transformations
        self.call_functions("temp_in.qasm", "temp_out.qasm")
        opt_circ = QuantumCircuit.from_qasm_file("temp_out.qasm")
        
        # convert back to a dag and return
        to_dag = circuit_to_dag(opt_circ)
        os.remove("temp_in.qasm")
        os.remove("temp_out.qasm")
        return to_dag
    
    def call_functions(self, inf, outf):
        v = VOQC(inf)
        for i in range(len(self.funcs)):
            if self.funcs[i] == "simple_map":
                if not (v.c_graph and v.layout):
                    print("'simple_map' requires the connectivity graph and layout to be set. Skipping this pass.")
                    continue
            call = getattr(v, self.funcs[i])
            call()
        v.write(outf)  
