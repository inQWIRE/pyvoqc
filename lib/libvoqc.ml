open Voqc.Qasm
open Voqc.Main

let () = Callback.register "read_qasm" read_qasm
let () = Callback.register "write_qasm" write_qasm

let ()  = Callback.register "count_I" count_I
let ()  = Callback.register "count_X" count_X
let ()  = Callback.register "count_Y" count_Y
let ()  = Callback.register "count_Z" count_Z
let ()  = Callback.register "count_H" count_H
let ()  = Callback.register "count_S" count_S
let ()  = Callback.register "count_T" count_T
let ()  = Callback.register "count_Sdg" count_Sdg
let ()  = Callback.register "count_Tdg" count_Tdg
let ()  = Callback.register "count_Rx" count_Rx
let ()  = Callback.register "count_Ry" count_Ry
let ()  = Callback.register "count_Rz" count_Rz
let ()  = Callback.register "count_Rzq" count_Rzq
let ()  = Callback.register "count_U1" count_U1
let ()  = Callback.register "count_U2" count_U2
let ()  = Callback.register "count_U3" count_U3
let ()  = Callback.register "count_CX" count_CX
let ()  = Callback.register "count_CZ" count_CZ
let ()  = Callback.register "count_SWAP" count_SWAP
let ()  = Callback.register "count_CCX" count_CCX
let ()  = Callback.register "count_CCZ" count_CCZ
let ()  = Callback.register "count_total" count_total
let ()  = Callback.register "count_rzq_clifford" count_rzq_clifford

let () = Callback.register "check_well_typed" check_well_typed
let () = Callback.register "convert_to_rzq" convert_to_rzq
let () = Callback.register "convert_to_ibm" convert_to_ibm
let () = Callback.register "decompose_to_cnot" decompose_to_cnot
let () = Callback.register "replace_rzq" replace_rzq

let () = Callback.register "optimize_ibm" optimize_ibm
let () = Callback.register "not_propagation" not_propagation
let () = Callback.register "hadamard_reduction" hadamard_reduction
let () = Callback.register "cancel_single_qubit_gates" cancel_single_qubit_gates
let () = Callback.register "cancel_two_qubit_gates" cancel_two_qubit_gates
let () = Callback.register "merge_rotations" merge_rotations
let () = Callback.register "optimize_nam" optimize_nam
let () = Callback.register "optimize" optimize_nam

let () = Callback.register "decompose_swaps" decompose_swaps
let () = Callback.register "trivial_layout" trivial_layout
let () = Callback.register "check_list" check_list
let () = Callback.register "list_to_layout" list_to_layout
let () = Callback.register "c_graph_from_coupling_map" c_graph_from_coupling_map
let () = Callback.register "check_swap_equivalence" check_swap_equivalence
let () = Callback.register "check_constraints" check_constraints