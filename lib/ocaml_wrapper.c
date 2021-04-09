#include <stdio.h>
#include <string.h>
#include <caml/mlvalues.h>
#include <caml/alloc.h>
#include <caml/memory.h>
#include <caml/fail.h>
#include <caml/callback.h>
#include "ocaml_wrapper.h"

// CLOSURE, wrap, destroy taken from https://github.com/xoolive/facile

#define CLOSURE(A)\
  static const value * closure = NULL;\
  if (closure == NULL) {\
    closure = caml_named_value(A);\
  }

value* wrap(value v) {
    CAMLparam1(v);
    value* res = (value*) malloc(sizeof(value));
    *res = v;
    caml_register_global_root(res);
    CAMLreturnT(value*, res);
}

void destroy(value* v) {
    caml_remove_global_root(v);
    free(v);
}

void init () {
    static char* dummy_argv[2] = { "", NULL };
    caml_startup(dummy_argv);
}

// For functions that take value* -> value*
#define RUNOPT(A,C)\
  CAMLparam0();\
  CAMLlocal1(res);\
  CLOSURE(A);\
  res = caml_callback(*closure, *C);\
  destroy(C);\
  CAMLreturnT(value*, wrap(res));

// Start of custom code for wrapping VOQC functions

// TODO: Why are we using value* instead of value everywhere? (I don't remember) -KH

CircIntPair read_qasm (char* fname) {
   CAMLparam0();
   CAMLlocal2(local, res);
   local = caml_copy_string(fname);
   CLOSURE("read_qasm");
   res = caml_callback(*closure, local);
   CircIntPair retval;
   retval.circ = wrap (Field (res, 0)); 
   retval.nqbits = Int_val (Field (res, 1));
   CAMLreturnT(CircIntPair, retval);
}

void write_qasm (value* circ, int nqbits, char* outf) {
   CAMLparam0(); // CAMLparam0 since we are passing value* rather than value
   CAMLlocal1(fname);
   fname = caml_copy_string(outf);
   CLOSURE("write_qasm");
   caml_callback3(*closure, *circ, Val_int(nqbits), fname);
   CAMLreturn0;
}

int count_I (value* circ) {
   CLOSURE("count_I");
   return Int_val(caml_callback(*closure, *circ));
}

int count_X (value* circ) {
   CLOSURE("count_X");
   return Int_val(caml_callback(*closure, *circ));
}

int count_Y (value* circ) {
   CLOSURE("count_Y");
   return Int_val(caml_callback(*closure, *circ));
}

int count_Z (value* circ) {
   CLOSURE("count_Z");
   return Int_val(caml_callback(*closure, *circ));
}

int count_H (value* circ) {
   CLOSURE("count_H");
   return Int_val(caml_callback(*closure, *circ));
}

int count_S (value* circ) {
   CLOSURE("count_S");
   return Int_val(caml_callback(*closure, *circ));
}

int count_T (value* circ) {
   CLOSURE("count_T");
   return Int_val(caml_callback(*closure, *circ));
}

int count_Sdg (value* circ) {
   CLOSURE("count_Sdg");
   return Int_val(caml_callback(*closure, *circ));
}

int count_Tdg (value* circ) {
   CLOSURE("count_Tdg");
   return Int_val(caml_callback(*closure, *circ));
}

int count_Rx (value* circ) {
   CLOSURE("count_Rx");
   return Int_val(caml_callback(*closure, *circ));
}

int count_Ry (value* circ) {
   CLOSURE("count_Ry");
   return Int_val(caml_callback(*closure, *circ));
}

int count_Rz (value* circ) {
   CLOSURE("count_Rz");
   return Int_val(caml_callback(*closure, *circ));
}

int count_Rzq (value* circ) {
   CLOSURE("count_Rzq");
   return Int_val(caml_callback(*closure, *circ));
}

int count_U1 (value* circ) {
   CLOSURE("count_U1");
   return Int_val(caml_callback(*closure, *circ));
}

int count_U2 (value* circ) {
   CLOSURE("count_U2");
   return Int_val(caml_callback(*closure, *circ));
}

int count_U3 (value* circ) {
   CLOSURE("count_U3");
   return Int_val(caml_callback(*closure, *circ));
}

int count_CX (value* circ) {
   CLOSURE("count_CX");
   return Int_val(caml_callback(*closure, *circ));
}

int count_CZ (value* circ) {
   CLOSURE("count_CZ");
   return Int_val(caml_callback(*closure, *circ));
}

int count_SWAP (value* circ) {
   CLOSURE("count_SWAP");
   return Int_val(caml_callback(*closure, *circ));
}

int count_CCX (value* circ) {
   CLOSURE("count_CCX");
   return Int_val(caml_callback(*closure, *circ));
}

int count_CCZ (value* circ) {
   CLOSURE("count_CCZ");
   return Int_val(caml_callback(*closure, *circ));
}

int count_clifford_rzq (value* circ) {
   CLOSURE("count_clifford_rzq");
   return Int_val(caml_callback(*closure, *circ));
}

int total_gate_count (value* circ) {
   CLOSURE("total_gate_count");
   return Int_val(caml_callback(*closure, *circ));
}

int check_well_typed (value* circ, int nqbits) {
    CLOSURE("check_well_typed");
    return Bool_val(caml_callback2(*closure, *circ, Val_int(nqbits)));
}

value* convert_to_rzq (value* circ) {
   RUNOPT("convert_to_rzq", circ);
}

value* convert_to_ibm (value* circ) {
   RUNOPT("convert_to_ibm", circ);
}

value* decompose_to_cnot (value* circ) {
   RUNOPT("decompose_to_cnot", circ);
}

value* replace_rzq (value* circ) {
   RUNOPT("replace_rzq", circ);
}

value* optimize_1q_gates (value* circ) {
   RUNOPT("optimize_1q_gates", circ);
}

value* cx_cancellation (value* circ) {
   RUNOPT("cx_cancellation", circ);
}

value* optimize_ibm (value* circ) {
   RUNOPT("optimize_ibm", circ);
}

value* not_propagation (value* circ) {
   RUNOPT("not_propagation", circ);
}

value* hadamard_reduction (value* circ) {
   RUNOPT("hadamard_reduction", circ);
}

value* cancel_single_qubit_gates (value* circ) {
   RUNOPT("cancel_single_qubit_gates", circ);
}

value* cancel_two_qubit_gates (value* circ) {
   RUNOPT("cancel_two_qubit_gates", circ);
}

value* merge_rotations (value* circ) {
   RUNOPT("merge_rotations", circ);
}

value* optimize_nam (value* circ) {
   RUNOPT("optimize_nam", circ);
}

int check_layout (value* layout, int nqbits) {
    CLOSURE("check_layout");
    return Bool_val(caml_callback2(*closure, *layout, Val_int(nqbits)));
}

int check_graph (value* c_graph) {
    CLOSURE("check_graph");
    return Bool_val(caml_callback(*closure, *c_graph));
}

int check_constraints (value* circ, value* c_graph) {
    CLOSURE("check_constraints");
    return Bool_val(caml_callback2(*closure, *circ, *c_graph));
}

CircLayoutPair simple_map (value* circ, value* layout, value* c_graph) {
    CAMLparam0();
    CAMLlocal1(res);
    CLOSURE("simple_map");
    res = caml_callback3(*closure, *circ, *layout, *c_graph);
    CircLayoutPair retval;
    retval.circ = wrap (Field (res, 0));
    retval.layout = wrap (Field (res, 1));
    CAMLreturnT(CircLayoutPair, retval);
}

value* make_tenerife () {
    CAMLparam0();
    CAMLlocal1(res);
    CLOSURE("make_tenerife");
    res = caml_callback(*closure, Val_unit);
    CAMLreturnT(value*, wrap(res));
}

value* make_lnn (int nqbits) {
    CAMLparam0();
    CAMLlocal1(res);
    CLOSURE("make_lnn");
    res = caml_callback(*closure, Val_int(nqbits));
    CAMLreturnT(value*, wrap(res));
}

value* make_lnn_ring (int nqbits) {
    CAMLparam0();
    CAMLlocal1(res);
    CLOSURE("make_lnn_ring");
    res = caml_callback(*closure, Val_int(nqbits));
    CAMLreturnT(value*, wrap(res));
}

value* make_grid (int nrows, int ncols) {
    CAMLparam0();
    CAMLlocal1(res);
    CLOSURE("make_grid");
    res = caml_callback2(*closure, Val_int(nrows), Val_int(ncols));
    CAMLreturnT(value*, wrap(res));
}

value* trivial_layout (int nqbits) {
    CAMLparam0();
    CAMLlocal1(res);
    CLOSURE("trivial_layout");
    res = caml_callback(*closure, Val_int(nqbits));
    CAMLreturnT(value*, wrap(res));
}

// buff is allocated & initialized in the Python code with nqbits entries
value* list_to_layout (int nqbits, int* buff) {
    CAMLparam0();
    CAMLlocal3(res, cons, lst);
    int i;
    for (i = nqbits - 1; i >= 0; i--) // build the list "backwards"
    {
        cons = caml_alloc(2, 0);
        Store_field(cons, 0, Val_int(buff[i]));  // head
        Store_field(cons, 1, lst);               // tail
        lst = cons;
    }
    CLOSURE("list_to_layout");
    res = caml_callback(*closure, lst);
    CAMLreturnT(value*, wrap(res));
}

// buff is allocated in the Python code with nqbits entries
void layout_to_list (value* layout, int nqbits, int* buff) {
    CAMLparam0();
    CAMLlocal2(res, head);
    CLOSURE("layout_to_list");
    res = caml_callback2(*closure, *layout, Val_int(nqbits));
    int* retval = malloc(nqbits * sizeof(int));
    int i;
    for (i = 0; i < nqbits; i++) {
        head = Field(res, 0); // head
        res = Field(res, 1);  // tail
        buff[i] = Int_val (head);
    }
    CAMLreturn0;
}


