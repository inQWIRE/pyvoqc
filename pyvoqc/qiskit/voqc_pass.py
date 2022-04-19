from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.transpiler.passmanager import PassManager
from qiskit.transpiler.passes import CheckMap
from qiskit.transpiler.passes import VF2Layout
from qiskit.transpiler.passes import TrivialLayout
from qiskit.transpiler.passes import DenseLayout
from qiskit.transpiler.passes import NoiseAdaptiveLayout
from qiskit.transpiler.passes import SabreLayout
from qiskit.transpiler.passes import BasicSwap
from qiskit.transpiler.passes import LookaheadSwap
from qiskit.transpiler.passes import StochasticSwap
from qiskit.transpiler.passes import SabreSwap
from qiskit.transpiler.passes import FullAncillaAllocation
from qiskit.transpiler.passes import EnlargeWithAncilla
from qiskit.transpiler.passes import ApplyLayout
from qiskit.transpiler.passes.layout.vf2_layout import VF2LayoutStopReason

from pyvoqc.voqc import get_library_handle, VOQCCircuit, VOQCError
import os

class VOQCOptimize(TransformationPass):
    '''
    Qiskit TransformationPass to run VOQC optimizations. 
    '''
    def __init__(self, opts):
        super().__init__()
        self.opts = opts
        self.defined_opts = [
            "optimize_ibm",
            "not_propagation",
            "hadamard_reduction",
            "cancel_single_qubit_gates",
            "cancel_two_qubit_gates",
            "merge_rotations",
            "optimize_nam",
            "optimize" ]
        self.voqc_gates = ['i', 'x', 'y', 'z', 'h', 's', 't', 'sdg', 'tdg', 'rx', 'ry', 
                           'rz', 'rzq', 'u1', 'u2', 'u3', 'cx', 'cz', 'swap', 'ccx', 'ccz']
        
        for opt in self.opts:
            if not (opt in self.defined_opts):
                raise VOQCError("Invalid VOQC optimization pass %s." % opt)
            
    def run(self, dag):
        # check that gates are supported in VOQC
        for node in dag.op_nodes():
            if not (node.name in self.voqc_gates):
                raise VOQCError("Unsupported gate %s." % node.name)

        if len(self.opts) > 0:
            # write qasm file 
            # TODO : would be nice if we could convert directly from Qiskit's circuit,
            #        but this requires support in the OCaml code
            circ = dag_to_circuit(dag)     
            circ.qasm(formatted=False, filename="temp_in.qasm")
            
            # apply VOQC transformations
            self.call_opts("temp_in.qasm", "temp_out.qasm")
            
            # convert back to a dag and return
            opt_circ = QuantumCircuit.from_qasm_file("temp_out.qasm")
            to_dag = circuit_to_dag(opt_circ)
            os.remove("temp_in.qasm")
            os.remove("temp_out.qasm")
            return to_dag
        
        else:
            return dag
    
    def call_opts(self, inf, outf):
        lib = get_library_handle()
        c = VOQCCircuit(lib, inf)
        for opt in self.opts:
            call = getattr(c, opt)
            call()
        c.replace_rzq() # always call replace RzQ in case a Nam pass is used
        c.write(outf)

class VOQCDecompose3q(TransformationPass):
    '''
    Qiskit TransformationPass using VOQC to decompose multi-qubit gates to CNOTs. 
    '''
    def __init__(self):
        super().__init__()
        self.voqc_gates = ['i', 'x', 'y', 'z', 'h', 's', 't', 'sdg', 'tdg', 'rx', 'ry', 
                           'rz', 'rzq', 'u1', 'u2', 'u3', 'cx', 'cz', 'swap', 'ccx', 'ccz']
            
    def run(self, dag):
        # check that gates are supported in VOQC
        for node in dag.op_nodes():
            if not (node.name in self.voqc_gates):
                raise VOQCError("Unsupported gate %s." % node.name)

        # write qasm file 
        circ = dag_to_circuit(dag)     
        circ.qasm(formatted=False, filename="temp_in.qasm")
        
        # apply VOQC transformations
        lib = get_library_handle()
        c = VOQCCircuit(lib, "temp_in.qasm")
        c.decompose_to_cnot()
        c.write("temp_out.qasm")

        # convert back to a dag and return
        circ = QuantumCircuit.from_qasm_file("temp_out.qasm")
        to_dag = circuit_to_dag(circ)
        os.remove("temp_in.qasm")
        os.remove("temp_out.qasm")
        return to_dag

class VOQCMap(TransformationPass):
    '''
    Qiskit TransformationPass to run Qiskit's mapping + VOQC translation validation. 
    '''
    def __init__(self, layout_method, routing_method, backend_properties, coupling_map, seed_transpiler):
        super().__init__()
        self.layout_method = layout_method
        self.routing_method = routing_method
        self.backend_properties = backend_properties
        self.coupling_map = coupling_map
        self.seed_transpiler = seed_transpiler
        self.voqc_gates = ['i', 'x', 'y', 'z', 'h', 's', 't', 'sdg', 'tdg', 'rx', 'ry', 
                    'rz', 'rzq', 'u1', 'u2', 'u3', 'cx', 'cz', 'swap', 'ccx', 'ccz']
            
    def run(self, dag):
        # check that gates are supported in VOQC
        for node in dag.op_nodes():
            if not (node.name in self.voqc_gates):
                raise VOQCError("Unsupported gate %s." % node.name)

        # save input circuit
        circ = dag_to_circuit(dag)     
        circ.qasm(formatted=False, filename="temp_in.qasm")
        
        # apply Qiskit layout/routing, adapted from Qiskit's level 3 pass manager
        # https://github.com/Qiskit/qiskit-terra/blob/main/qiskit/transpiler/preset_passmanagers/level3.py
        # TODO: Is it ok to use a PassManager inside of a TransformationPass?
        def _vf2_match_not_found(property_set):
            if property_set["layout"] is None:
                return True
            if (
                property_set["VF2Layout_stop_reason"] is not None
                and property_set["VF2Layout_stop_reason"] is not VF2LayoutStopReason.SOLUTION_FOUND
            ):
                return True
            return False
        
        _choose_layout_0 = VF2Layout(
                                self.coupling_map,
                                seed=self.seed_transpiler,
                                call_limit=int(3e7),
                                time_limit=60,
                                properties=self.backend_properties,
                            )

        if self.layout_method == "trivial":
            _choose_layout_1 = TrivialLayout(self.coupling_map)
        elif self.layout_method == "dense":
            _choose_layout_1 = DenseLayout(self.coupling_map, self.backend_properties)
        elif self.layout_method == "noise_adaptive":
            _choose_layout_1 = NoiseAdaptiveLayout(self.backend_properties)
        elif self.layout_method == "sabre":
            _choose_layout_1 = SabreLayout(self.coupling_map, max_iterations=4, seed=self.seed_transpiler)
        else:
            raise VOQCError("Invalid layout method %s." % self.layout_method)

        _embed = [FullAncillaAllocation(self.coupling_map), EnlargeWithAncilla(), ApplyLayout()]

        _swap_check = CheckMap(self.coupling_map)

        def _swap_condition(property_set):
            return not property_set["is_swap_mapped"]

        if self.routing_method == "basic":
            _swap = [BasicSwap(self.coupling_map)]
        elif self.routing_method == "stochastic":
            _swap = [StochasticSwap(self.coupling_map, trials=200, seed=self.seed_transpiler)]
        elif self.routing_method == "lookahead":
            _swap = [LookaheadSwap(self.coupling_map, search_depth=5, search_width=6)]
        elif self.routing_method == "sabre":
            _swap = [SabreSwap(self.coupling_map, heuristic="decay", seed=self.seed_transpiler)]
        else:
            raise VOQCError("Invalid routing method %s." % self.routing_method)

        pm = PassManager()
        pm.append(_choose_layout_0)
        pm.append(_choose_layout_1, condition=_vf2_match_not_found)
        pm.append(_embed)
        pm.append(_swap_check)
        pm.append(_swap, condition=_swap_condition)
        
        mapped_circ = pm.run(circ)

        # save post-mapping circuit
        mapped_circ.qasm(formatted=False, filename="temp_out.qasm")

        # apply VOQC mapping validation
        lib = get_library_handle()
        c1 = VOQCCircuit(lib, "temp_in.qasm")
        c1.trivial_layout(self.coupling_map.size())
        c2 = VOQCCircuit(lib, "temp_out.qasm")
        c2.list_to_layout(self.get_layout_list(mapped_circ))
        if c1.check_swap_equivalence(c2) != 1:
            raise VOQCError("Circuit mapping validation failed (input and output are not equivalent).")

        # apply VOQC SWAP decomposition
        c2.c_graph_from_coupling_map(self.coupling_map.size(), self.coupling_map.get_edges())
        c2.decompose_swaps()

        # check that connectivity constraints are satisfied
        if c2.check_constraints() != 1:
            raise VOQCError("Circuit mapping validation failed (connectivity constraints not satisfied).")
        c2.write("temp_out2.qasm")

        # convert back to a dag and return
        circ = QuantumCircuit.from_qasm_file("temp_out2.qasm")
        to_dag = circuit_to_dag(circ)
        os.remove("temp_in.qasm")
        os.remove("temp_out.qasm")
        os.remove("temp_out2.qasm")
        return to_dag

    def get_layout_list(self, circ):
        layout = circ._layout
        regs = layout.get_registers()
        qs = [r for r in regs if r.name != "ancilla"]
        anc = [r for r in regs if r.name == "ancilla"]
        if (len(qs) != 1 or len(anc) > 1):
            raise VOQCError("Failed to convert mapped circuit's layout to a list.")
        base = qs[0].size
        bits = layout.get_physical_bits()
        out = []
        for i in range(len(bits)):
            if bits[i] in qs[0]:
                out.append(qs[0].index(bits[i]))
            else:
                out.append(base + anc[0].index(bits[i]))
        return out

def voqc_pass_manager(pre_opts=None, post_opts=None, layout_method=None, routing_method=None, backend_properties=None, coupling_map=None, seed_transpiler=None) -> PassManager:
    """
    VOQC pass manager. Performs Qiskit layout/routing and VOQC translation validation 
    followed by the specified VOQC optimizations.
    
        Parameters:
            pre_opts: sequence of VOQC optimizations to apply before mapping (default is [])
            post_opts: sequence of VOQC optimizations to apply after mapping (default is [optimize])
            layout_method: Qiskit method to use for layout (default is sabre, VF2Layout is always tried first)
            routing_method: Qiskit method to use for routing (default is sabre)
            backend_properties: backend properties, used for layout/routing
            coupling_map: CNOT connectivity graph, used for layout/routing
            seed_transpiler: seed for randomness, used for layout/routing
     
        Returns:
            A Qiskit pass manager

        Notes: 
            The output gate set depends on the sequence on optimizations applied. 
            By default, output will use the gate set {U1, U2, U3, CX}
            If the coupling_map is None, only optimizations will be applied.
            If the optimization list is empty, only mapping will be applied.
    """
    pre_opts = pre_opts or []
    post_opts = post_opts or ["optimize"]
    layout_method = layout_method or "sabre"
    routing_method = routing_method or "sabre"

    pm = PassManager()

    pm.append(VOQCOptimize(pre_opts))

    if coupling_map:
        pm.append(VOQCDecompose3q())
        pm.append(VOQCMap(layout_method, routing_method, backend_properties, coupling_map, seed_transpiler))

    pm.append(VOQCOptimize(post_opts))

    return pm