open Voqc.Qasm
open Voqc.Main

(* Rather than writing (fun x y -> foo x y), we could just write "foo". But listing
   the arguments helps me keep organized. -KH *)
let () = Callback.register "read_qasm" (fun fname -> read_qasm fname)
let () = Callback.register "write_qasm" (fun c nqbits fname -> write_qasm c nqbits fname)

(* TODO: I will expose every count_<G> function in Voqc's next opam release. 
   For now, a dumb fix. -KH *)
let ()  = Callback.register "count_I" 
  (fun c -> match count_gates c 
            with BuildCounts (x, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_X"
  (fun c -> match count_gates c 
            with BuildCounts (_, x, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_Y"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, x, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_Z"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, x, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_H"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, x, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_S"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, x, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_T"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, x, _, _, _, _, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_Sdg"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, x, _, _, _, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_Tdg"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, x, _, _, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_Rx" 
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, x, _, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_Ry"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, x, _, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_Rz"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, _, x, _, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_Rzq"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, _, _, x, _, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_U1"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, _, _, _, x, _, _, _, _, _, _, _) -> x)
let ()  = Callback.register "count_U2"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, _, _, _, _, x, _, _, _, _, _, _) -> x) 
let ()  = Callback.register "count_U3"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, x, _, _, _, _, _) -> x)
let ()  = Callback.register "count_CX"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, x, _, _, _, _) -> x)
let ()  = Callback.register "count_CZ"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, x, _, _, _) -> x)
let ()  = Callback.register "count_SWAP"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, x, _, _) -> x)
let ()  = Callback.register "count_CCX"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, x, _) -> x)
let ()  = Callback.register "count_CCZ"
  (fun c -> match count_gates c 
            with BuildCounts (_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, x) -> x)
let ()  = Callback.register "count_clifford_rzq" count_clifford_rzq 
let ()  = Callback.register "total_gate_count" total_gate_count 
let () = Callback.register "check_well_typed" check_well_typed
let () = Callback.register "convert_to_rzq" convert_to_rzq
let () = Callback.register "convert_to_ibm" convert_to_ibm
let () = Callback.register "decompose_to_cnot" decompose_to_cnot
let () = Callback.register "replace_rzq" replace_rzq

let () = Callback.register "optimize_1q_gates" optimize_1q_gates
let () = Callback.register "cx_cancellation" cx_cancellation
let () = Callback.register "optimize_ibm" optimize_ibm
let () = Callback.register "not_propagation" not_propagation
let () = Callback.register "hadamard_reduction" hadamard_reduction
let () = Callback.register "cancel_single_qubit_gates" cancel_single_qubit_gates
let () = Callback.register "cancel_two_qubit_gates" cancel_two_qubit_gates
let () = Callback.register "merge_rotations" merge_rotations
let () = Callback.register "optimize_nam" optimize_nam

let () = Callback.register "check_layout" (fun la n -> check_layout la n)
let () = Callback.register "check_graph" check_graph
let () = Callback.register "check_constraints" (fun c cg -> check_constraints c cg)
let () = Callback.register "simple_map" (fun c la cg -> simple_map c la cg)
let () = Callback.register "make_tenerife" make_tenerife
let () = Callback.register "make_lnn" make_lnn
let () = Callback.register "make_lnn_ring" make_lnn_ring
let () = Callback.register "make_grid" make_grid
let () = Callback.register "trivial_layout" trivial_layout
let () = Callback.register "list_to_layout" list_to_layout
let () = Callback.register "layout_to_list" (fun la n -> layout_to_list la n)
