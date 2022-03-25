#include <stdio.h>
#include <string.h>
#include <caml/mlvalues.h>
#include <caml/alloc.h>
#include <caml/memory.h>
#include <caml/fail.h>
#include <caml/callback.h>
#include "ocaml_wrapper.h"

/* From the OCaml Reference Manual:

"Living in Harmony with the Garbage Collector"

Rule ‍1  A function that has parameters or local variables of type value must 
        begin with a call to one of the CAMLparam macros and return with CAMLreturn, 
        CAMLreturn0, or CAMLreturnT. In particular, CAMLlocal and CAMLxparam can only 
        be called after CAMLparam.
Rule ‍2  Local variables of type value must be declared with one of the CAMLlocal macros. 
        Arrays of values are declared with CAMLlocalN. These macros must be used at the 
        beginning of the function, not in a nested block.
Rule ‍3  Assignments to the fields of structured blocks must be done with the Store_field 
        macro (for normal blocks) or Store_double_field macro (for arrays and records of 
        floating-point numbers). Other assignments must not use Store_field nor 
        Store_double_field.
Rule ‍4  Global variables containing values must be registered with the garbage collector 
        using the caml_register_global_root function, save that global variables and 
        locations that will only ever contain OCaml integers (and never pointers) do not 
        have to be registered.
*/

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

int count_total (value* circ) {
   CLOSURE("count_total");
   return Int_val(caml_callback(*closure, *circ));
}

int count_rzq_clifford (value* circ) {
   CLOSURE("count_rzq_clifford");
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

value* optimize (value* circ) {
   RUNOPT("optimize", circ);
}

value* decompose_swaps(value* circ, value* c_graph) {
    CAMLparam0();
    CAMLlocal1(res);
    CLOSURE("decompose_swaps");
    res = caml_callback2(*closure, *circ, *c_graph);
    destroy(circ);
    CAMLreturnT(value*, wrap(res));
}

value* trivial_layout (int nqbits) {
    CAMLparam0();
    CAMLlocal1(res);
    CLOSURE("trivial_layout");
    res = caml_callback(*closure, Val_int(nqbits));
    CAMLreturnT(value*, wrap(res));
}

int check_list(int nqbits, int* buff) {
    CAMLparam0();
    CAMLlocal2(cons, lst);
    int i;
    for (i = nqbits - 1; i >= 0; i--) // build the list "backwards"
    {
        cons = caml_alloc(2, 0);
        Store_field(cons, 0, Val_int(buff[i]));  // head
        Store_field(cons, 1, lst);               // tail
        lst = cons;
    }
    CLOSURE("check_list");
    CAMLreturnT(int, Bool_val(caml_callback(*closure, lst)));
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

value* c_graph_from_coupling_map(int nqbits, int len, IntIntPair* coupling_map) {
    CAMLparam0();
    CAMLlocal4(res, cons, lst, tup);
    int i;
    for (i = len - 1; i >= 0; i--)
    {
        cons = caml_alloc(2, 0);
        tup = caml_alloc(2, 0);
        Store_field(tup, 0, Val_int(coupling_map[i].x)); // fst elem of the tuple
        Store_field(tup, 1, Val_int(coupling_map[i].y)); // snd elem of the tuple
        Store_field(cons, 0, tup); // head
        Store_field(cons, 1, lst); // tail
        lst = cons;
    }
    CLOSURE("c_graph_from_coupling_map");
    res = caml_callback2(*closure, nqbits, lst);
    CAMLreturnT(value*, wrap(res));
}

int check_swap_equivalence (value* circ1, value* circ2, value* layout1, value* layout2) {
    CAMLparam0();
    CAMLlocalN(args, 4);
    CLOSURE("check_swap_equivalence");
    args[0] = *circ1;
    args[1] = *circ2;
    args[2] = *layout1;
    args[3] = *layout2;
    CAMLreturnT(int, Bool_val(caml_callbackN(*closure, 4, args)));
}

int check_constraints (value* circ, value* c_graph) {
    CLOSURE("check_constraints");
    return Bool_val(caml_callback2(*closure, *circ, *c_graph));
}