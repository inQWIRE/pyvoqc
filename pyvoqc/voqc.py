from ctypes import *
import os.path
import time

class VOQCError(Exception):
    def __init__(self, *message):
        super().__init__(" ".join(message))
        self.message = " ".join(message)
    def __str__(self):
        return repr(self.message)

class CircIntPair(Structure):
    _fields_ = [('circ', c_void_p),
                ('nqbits', c_int)] 

class IntIntPair(Structure):
    _fields_ = [('x', c_int),
                ('y', c_int)] 

def filter_counts(counts):
    cpy = dict()
    for (key, value) in counts.items():
        if value > 0:
            cpy[key] = value
    return cpy

# NOTE: This function should only be called once, so it can't be inside the
# Circuit class initializer, which may be called multiple times. I'm not sure 
# what the best solution is. -KH
def get_library_handle():
    # set path and lib
    rel = os.path.dirname(os.path.abspath(__file__)) # ..
    lib = CDLL(os.path.join(rel,'lib/libvoqc.so'))

    # initialize OCaml code
    lib.init.argtypes = None
    lib.init.restype= None
    lib.init()

    return lib

class VOQCCircuit:
    
    # Constructor takes a library handle & qasm file as input
    def __init__(self, handle, fname):

        self.lib = handle

        # call read_qasm function and return pointer to a circuit 
        self.lib.read_qasm.argtypes = [c_char_p]
        self.lib.read_qasm.restype = CircIntPair      
        res = self.lib.read_qasm(fname.encode('utf-8'))
        self.circ = res.circ
        self.nqbits = res.nqbits
        
        # start with an empty layout and connectivity graph
        self.layout = None
        self.c_graph = None
        
    # Destructor
    def __del__(self):
        # free OCaml root
        self.lib.destroy.argtypes = [c_void_p]
        self.lib.destroy.restype = None
        self.lib.destroy(self.circ) 
        if self.layout: self.lib.destroy(self.layout)
        if self.c_graph: self.lib.destroy(self.c_graph)   

    def write(self, fname):

        # define function argtype/restype to match C
        self.lib.write_qasm.argtypes = [c_void_p, c_int, c_char_p]
        self.lib.write_qasm.restype = None
                
        # write qasm file
        self.lib.write_qasm(self.circ, self.nqbits, fname.encode('utf-8'))

    def count_gates(self):        
        self.lib.count_I.argtypes = [c_void_p]
        self.lib.count_I.restype = c_int
        self.lib.count_X.argtypes = [c_void_p]
        self.lib.count_X.restype = c_int
        self.lib.count_Y.argtypes = [c_void_p]
        self.lib.count_Y.restype = c_int
        self.lib.count_Z.argtypes = [c_void_p]
        self.lib.count_Z.restype = c_int
        self.lib.count_H.argtypes = [c_void_p]
        self.lib.count_H.restype = c_int
        self.lib.count_S.argtypes = [c_void_p]
        self.lib.count_S.restype = c_int
        self.lib.count_T.argtypes = [c_void_p]
        self.lib.count_T.restype = c_int
        self.lib.count_Sdg.argtypes = [c_void_p]
        self.lib.count_Sdg.restype = c_int
        self.lib.count_Tdg.argtypes = [c_void_p]
        self.lib.count_Tdg.restype = c_int
        self.lib.count_Rx.argtypes = [c_void_p]
        self.lib.count_Rx.restype = c_int
        self.lib.count_Ry.argtypes = [c_void_p]
        self.lib.count_Ry.restype = c_int
        self.lib.count_Rz.argtypes = [c_void_p]
        self.lib.count_Rz.restype = c_int
        self.lib.count_Rzq.argtypes = [c_void_p]
        self.lib.count_Rzq.restype = c_int
        self.lib.count_U1.argtypes = [c_void_p]
        self.lib.count_U1.restype = c_int
        self.lib.count_U2.argtypes = [c_void_p]
        self.lib.count_U2.restype = c_int
        self.lib.count_U3.argtypes = [c_void_p]
        self.lib.count_U3.restype = c_int
        self.lib.count_CX.argtypes = [c_void_p]
        self.lib.count_CX.restype = c_int
        self.lib.count_CZ.argtypes = [c_void_p]
        self.lib.count_CZ.restype = c_int
        self.lib.count_SWAP.argtypes = [c_void_p]
        self.lib.count_SWAP.restype = c_int
        self.lib.count_CCX.argtypes = [c_void_p]
        self.lib.count_CCX.restype = c_int
        self.lib.count_CCZ.argtypes = [c_void_p]
        self.lib.count_CCZ.restype = c_int
        cnts = { "I" : self.lib.count_I(self.circ),
                 "X" : self.lib.count_X(self.circ),
                 "Y" : self.lib.count_Y(self.circ),
                 "Z" : self.lib.count_Z(self.circ),
                 "H" : self.lib.count_H(self.circ),
                 "S" : self.lib.count_S(self.circ),
                 "T" : self.lib.count_T(self.circ),
                 "Sdg" : self.lib.count_Sdg(self.circ),
                 "Tdg" : self.lib.count_Tdg(self.circ),
                 "Rx" : self.lib.count_Rx(self.circ),
                 "Ry" : self.lib.count_Ry(self.circ),
                 "Rz" : self.lib.count_Rz(self.circ),
                 "Rzq" : self.lib.count_Rzq(self.circ),
                 "U1" : self.lib.count_U1(self.circ),
                 "U2" : self.lib.count_U2(self.circ),
                 "U3" : self.lib.count_U3(self.circ),
                 "CX" : self.lib.count_CX(self.circ),
                 "CZ" : self.lib.count_CZ(self.circ),
                 "SWAP" : self.lib.count_SWAP(self.circ),
                 "CCX" : self.lib.count_CCX(self.circ),
                 "CCZ" : self.lib.count_CCZ(self.circ) }
        return filter_counts(cnts)

    def count_rzq_clifford(self):
        self.lib.count_rzq_clifford.argtypes = [c_void_p]
        self.lib.count_rzq_clifford.restype = c_int
        return self.lib.count_rzq_clifford(self.circ)

    def total_gate_count(self):
        self.lib.count_total.argtypes = [c_void_p]
        self.lib.count_total.restype = c_int
        return self.lib.count_total(self.circ)

    def print_info(self):
        print("Circuit uses %d qubits and %d gates." % (self.nqbits,self.total_gate_count()))
        print(self.count_gates())
        if self.layout:
            l = self.layout_to_list()
            print("Current layout is [%s]" % ",".join([str(i) for i in l]))
        else:
            print("No current layout.")

    def check_well_typed(self, nqbits):
        if nqbits != self.nqbits:
            print("Warning: the provided value of nqbits was %d, but the value of self.nqbits is %d." % (nqbits, self.nqbits))
        self.lib.check_well_typed.argtypes = [c_void_p, c_int]
        self.lib.check_well_typed.restype = c_int
        return (self.lib.check_well_typed(self.circ, nqbits) == 1)

    def convert_to_rzq(self):        
        self.lib.convert_to_rzq.argtypes = [c_void_p]
        self.lib.convert_to_rzq.restype = c_void_p
        self.circ = self.lib.convert_to_rzq(self.circ)
        return self

    def convert_to_ibm(self):        
        self.lib.convert_to_ibm.argtypes = [c_void_p]
        self.lib.convert_to_ibm.restype = c_void_p
        self.circ = self.lib.convert_to_ibm(self.circ)
        return self

    def decompose_to_cnot(self):        
        self.lib.decompose_to_cnot.argtypes = [c_void_p]
        self.lib.decompose_to_cnot.restype = c_void_p
        self.circ = self.lib.decompose_to_cnot(self.circ)
        return self
        
    def replace_rzq(self):        
        self.lib.replace_rzq.argtypes = [c_void_p]
        self.lib.replace_rzq.restype = c_void_p
        self.circ = self.lib.replace_rzq(self.circ)
        return self

    def optimize_ibm(self):        
        self.lib.optimize_ibm.argtypes = [c_void_p]
        self.lib.optimize_ibm.restype = c_void_p
        self.circ = self.lib.optimize_ibm(self.circ)
        return self

    def not_propagation(self):        
        self.lib.not_propagation.argtypes = [c_void_p]
        self.lib.not_propagation.restype = c_void_p
        self.circ = self.lib.not_propagation(self.circ)
        return self
    
    def hadamard_reduction(self):        
        self.lib.hadamard_reduction.argtypes = [c_void_p]
        self.lib.hadamard_reduction.restype = c_void_p
        self.circ = self.lib.hadamard_reduction(self.circ)
        return self
        
    def cancel_single_qubit_gates(self):        
        self.lib.cancel_single_qubit_gates.argtypes = [c_void_p]
        self.lib.cancel_single_qubit_gates.restype = c_void_p
        self.circ = self.lib.cancel_single_qubit_gates(self.circ)
        return self
        
    def cancel_two_qubit_gates(self):        
        self.lib.cancel_two_qubit_gates.argtypes = [c_void_p]
        self.lib.cancel_two_qubit_gates.restype = c_void_p
        self.circ = self.lib.cancel_two_qubit_gates(self.circ)
        return self
        
    def merge_rotations(self):        
        self.lib.merge_rotations.argtypes = [c_void_p]
        self.lib.merge_rotations.restype = c_void_p
        self.circ = self.lib.merge_rotations(self.circ)
        return self
        
    def optimize_nam(self):        
        self.lib.optimize_nam.argtypes = [c_void_p]
        self.lib.optimize_nam.restype = c_void_p
        self.circ = self.lib.optimize_nam(self.circ)
        return self

    def optimize(self):        
        self.lib.optimize.argtypes = [c_void_p]
        self.lib.optimize.restype = c_void_p
        self.circ = self.lib.optimize(self.circ)
        return self
    
    def decompose_swaps(self):
        if not self.c_graph: 
            raise VOQCError("Cannot apply decompose_swaps. Connectivity graph is not set.")
        else:
            self.lib.decompose_swaps.argtypes = [c_void_p, c_void_p]
            self.lib.decompose_swaps.restype = c_void_p
            self.circ = self.lib.decompose_swaps(self.circ, self.c_graph)    
            return self

    def trivial_layout(self, nqbits): 
        if self.nqbits > nqbits:
            raise VOQCError("The layout is too small. It must contain at least %d qubits." % self.nqbits)
        else:
            self.lib.trivial_layout.argtypes = [c_int]
            self.lib.trivial_layout.restype = c_void_p 
            self.layout = self.lib.trivial_layout(nqbits)
            self.nqbits = nqbits
            
    def list_to_layout(self, l):
        if self.nqbits > len(l):
            raise VOQCError("The layout is too small. The layout must contain at least %d qubits." % self.nqbits)
        else:
            arr = (c_int * len(l))(*l)
            self.lib.check_list.argtypes = [c_int, POINTER(c_int)]
            self.lib.check_list.restype = c_int
            if self.lib.check_list(len(l), arr) == 1:
                self.lib.list_to_layout.argtypes = [c_int, POINTER(c_int)]
                self.lib.list_to_layout.restype = c_void_p 
                self.layout = self.lib.list_to_layout(len(l), arr)
                self.nqbits = len(l)
            else:
                raise VOQCError("list_to_layout input list is invalid: %s." % l)

    def c_graph_from_coupling_map(self, nqbits, coupling_map):
        if self.nqbits > nqbits:
            raise VOQCError("The coupling map is too small. The connectivity graph must contain at least %d qubits." % self.nqbits)
        self.lib.destroy.argtypes = [c_void_p]
        self.lib.destroy.restype = None
        if self.c_graph:
            print("Warning: Deleting old connectivity graph.")
            self.lib.destroy(self.c_graph)
        arr = (IntIntPair * len(coupling_map))()
        for i in range(len(coupling_map)):
            arr[i].x = coupling_map[i][0]
            arr[i].y = coupling_map[i][1]
        self.lib.c_graph_from_coupling_map.argtypes = [c_int, c_int, POINTER(IntIntPair)]
        self.lib.c_graph_from_coupling_map.restype = c_void_p 
        self.c_graph = self.lib.c_graph_from_coupling_map(nqbits, len(coupling_map), arr)
        self.nqbits = nqbits

    def check_swap_equivalence(self, obj):
        if not self.layout or not obj.layout: 
            raise VOQCError("Cannot apply check_swap_equivalence. Input layouts are not set.")
        self.lib.check_swap_equivalence.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
        self.lib.check_swap_equivalence.restype = c_int
        return (self.lib.check_swap_equivalence(self.circ, obj.circ, self.layout, obj.layout) == 1)

    def check_constraints(self):
        if not self.c_graph:
            raise VOQCError("Cannot apply check_constraints. Connectivity graph is not set.")
        else:
            self.lib.check_constraints.argtypes = [c_void_p, c_void_p]
            self.lib.check_constraints.restype = c_int
            return (self.lib.check_constraints(self.circ, self.c_graph) == 1)

