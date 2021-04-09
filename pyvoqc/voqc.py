from ctypes import *
import os.path
import time

class CircIntPair(Structure):
    _fields_ = [('circ', c_void_p),
                ('nqbits', c_int)] 

class CircLayoutPair(Structure):
    _fields_ = [('circ', c_void_p),
                ('layout', c_void_p)] 

def filter_counts(counts):
    cpy = dict()
    for (key, value) in counts.items():
        if value > 0:
            cpy[key] = value
    return cpy

class VOQC:
    
    # Constructor (takes a qasm file as input)
    def __init__(self, fname):
        
        # set path and lib
        rel = os.path.dirname(os.path.abspath(__file__)) # ..
        self.lib = CDLL(os.path.join(rel,'lib/libvoqc.so'))

        # initialize OCaml code
        self.lib.init.argtypes = None
        self.lib.init.restype= None
        self.lib.init()

        # call read_qasm function and return pointer to a circuit 
        self.lib.read_qasm.argtypes = [c_char_p]
        self.lib.read_qasm.restype = CircIntPair      
        res = self.lib.read_qasm(fname.encode('utf-8'))
        self.circ = res.circ
        self.nqbits = res.nqbits
        
        # set layout and connectivity graph to Nil
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

    def count_clifford_rzq(self):
        self.lib.count_clifford_rzq.argtypes = [c_void_p]
        self.lib.count_clifford_rzq.restype = c_int
        return self.lib.count_clifford_rzq(self.circ)

    def total_gate_count(self):
        self.lib.total_gate_count.argtypes = [c_void_p]
        self.lib.total_gate_count.restype = c_int
        return self.lib.total_gate_count(self.circ)

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

    def optimize_1q_gates(self):        
        self.lib.optimize_1q_gates.argtypes = [c_void_p]
        self.lib.optimize_1q_gates.restype = c_void_p
        self.circ = self.lib.optimize_1q_gates(self.circ)
        return self

    def cx_cancellation(self):        
        self.lib.cx_cancellation.argtypes = [c_void_p]
        self.lib.cx_cancellation.restype = c_void_p
        self.circ = self.lib.cx_cancellation(self.circ)
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

    def check_layout(self):
        if not self.layout:
            print("Layout is not set. Call 'trivial_layout' or 'layout_from_list'.")
        else:
            self.lib.check_layout.argtypes = [c_void_p, c_int]
            self.lib.check_layout.restype = c_int
            return (self.lib.check_layout(self.layout, self.nqbits) == 1)
            
    def check_graph(self):
        if not self.c_graph:
            print("Connectivity graph is not set.")
        else:
            self.lib.check_graph.argtypes = [c_void_p]
            self.lib.check_graph.restype = c_int
            return (self.lib.check_graph(self.c_graph) == 1)
    
    def check_constraints(self):
        if not self.c_graph:
            print("Connectivity graph is not set.")
        else:
            self.lib.check_constraints.argtypes = [c_void_p, c_void_p]
            self.lib.check_constraints.restype = c_int
            return (self.lib.check_constraints(self.circ, self.c_graph) == 1)

    def make_tenerife(self):
        self.lib.destroy.argtypes = [c_void_p]
        self.lib.destroy.restype = None
        
        if self.c_graph: # delete old c_graph
            self.lib.destroy(self.c_graph)

        self.lib.make_tenerife.argtypes = None
        self.lib.make_tenerife.restype = c_void_p
        self.c_graph = self.lib.make_tenerife()
        
        # set the number of qubits to 5 and invalidate the previous layout
        self.nqbits = 5
        if self.layout:
            print("Deleting old layout. You will need to provide a new layout.")
            self.lib.destroy(self.layout)
            self.layout = None
    
    def make_lnn(self, nqbits):        
        self.lib.destroy.argtypes = [c_void_p]
        self.lib.destroy.restype = None
        if self.c_graph:
            self.lib.destroy(self.c_graph)
        self.lib.make_lnn.argtypes = [c_int]
        self.lib.make_lnn.restype = c_void_p
        self.c_graph = self.lib.make_lnn(nqbits)
        self.nqbits = nqbits
        if self.layout:
            print("Deleting old layout. You will need to provide a new layout.")
            self.lib.destroy(self.layout)
            self.layout = None

    def make_lnn_ring(self, nqbits):        
        self.lib.destroy.argtypes = [c_void_p]
        self.lib.destroy.restype = None
        if self.c_graph:
            self.lib.destroy(self.c_graph)
        self.lib.make_lnn_ring.argtypes = [c_int]
        self.lib.make_lnn_ring.restype = c_void_p
        self.c_graph = self.lib.make_lnn_ring(nqbits)
        self.nqbits = nqbits
        if self.layout:
            print("Deleting old layout. You will need to provide a new layout.")
            self.lib.destroy(self.layout)
            self.layout = None

    def make_grid(self, nrows, ncols):        
        self.lib.destroy.argtypes = [c_void_p]
        self.lib.destroy.restype = None
        if self.c_graph:
            self.lib.destroy(self.c_graph)
        self.lib.make_grid.argtypes = [c_int, c_int]
        self.lib.make_grid.restype = c_void_p
        self.c_graph = self.lib.make_grid(nrows, ncols)
        self.nqbits = nrows * ncols
        if self.layout:
            print("Deleting old layout. You will need to provide a new layout.")
            self.lib.destroy(self.layout)
            self.layout = None

    def trivial_layout(self, nqbits):
        if not self.c_graph:
            print("Please set the connectivity graph before the layout.")    
        elif self.nqbits != nqbits:
            print("The layout must contain %d qubits." % self.nqbits) 
        else:
            self.lib.trivial_layout.argtypes = [c_int]
            self.lib.trivial_layout.restype = c_void_p 
            self.layout = self.lib.trivial_layout(nqbits)
            self.nqbits = nqbits
    
    def layout_to_list(self):
        if not self.layout:
            print("Layout is not set. Call 'trivial_layout' or 'layout_from_list'.")
        else:
            arr = (c_int * self.nqbits)()
            self.lib.layout_to_list.argtypes = [c_void_p, c_int, POINTER(c_int)]
            self.lib.layout_to_list.restype = None
            self.lib.layout_to_list(self.layout, self.nqbits, arr)
            l = []
            for elmt in arr:
                l.append(elmt)
            return l
            
    def list_to_layout(self, l):
        if not self.c_graph:
            print("Please set the connectivity graph before the layout.")    
        elif self.nqbits != len(l):
            print("The layout must contain %d qubits." % self.nqbits) 
        else:
            arr = (c_int * len(l))(*l)
            self.lib.list_to_layout.argtypes = [c_int, POINTER(c_int)]
            self.lib.list_to_layout.restype = c_void_p 
            self.layout = self.lib.list_to_layout(len(l), arr)
            self.nqbits = len(l)
            if not self.check_layout():
                print("Warning: the generated layout is not well-formed (make sure list elements are unique).")
    
    def simple_map(self):
        if (not self.layout) or (not self.c_graph): 
            print("Layout or connectivity graph is not set.")
        else:
            self.lib.simple_map.argtypes = [c_void_p, c_void_p, c_void_p]
            self.lib.simple_map.restype = CircLayoutPair
            res = self.lib.simple_map(self.circ, self.layout, self.c_graph)    
            self.circ = res.circ 
            self.layout = res.layout
            return self  
    
