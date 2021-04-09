#include <caml/mlvalues.h>

void init();
void destroy(value*);

typedef struct circ_int_pair
{
  value* circ;
  int nqbits;
} CircIntPair ;

typedef struct circ_layout_pair
{
  value* circ;
  value* layout;
} CircLayoutPair ;


// I/O 
CircIntPair read_qasm(char* fname);
void write_qasm(value* circ, int nqbits, char* outf);

// Utility
int count_I(value* circ);
int count_X(value* circ);
int count_Y(value* circ);
int count_Z(value* circ);
int count_H(value* circ);
int count_S(value* circ);
int count_T(value* circ);
int count_Sdg(value* circ);
int count_Tdg(value* circ);
int count_Rx(value* circ);
int count_Ry(value* circ);
int count_Rz(value* circ);
int count_Rzq(value* circ);
int count_U1(value* circ);
int count_U2(value* circ);
int count_U3(value* circ);
int count_CX(value* circ);
int count_CZ(value* circ);
int count_SWAP(value* circ);
int count_CCX(value* circ);
int count_CCZ(value* circ);
int count_clifford_rzq(value* circ);
int total_gate_count(value* circ);
int check_well_typed(value* circ, int nqbits);
value* convert_to_rzq(value* circ);
value* convert_to_ibm(value* circ);
value* decompose_to_cnot(value* circ);
value* replace_rzq(value* circ);

// Optimization
value* optimize_1q_gates(value* circ);
value* cx_cancellation(value* circ);
value* optimize_ibm(value* circ);
value* not_propagation(value* circ);
value* hadamard_reduction(value* circ);
value* cancel_single_qubit_gates(value* circ);
value* cancel_two_qubit_gates(value* circ);
value* merge_rotations(value* circ);
value* optimize_nam(value* circ);

// Mapping
int check_layout(value* layout, int nqbits);
int check_graph(value* c_graph);
int check_constraints(value* circ, value* c_graph);
CircLayoutPair simple_map(value* circ, value* layout, value* c_graph);
value* make_tenerife();
value* make_lnn(int nqbits);
value* make_lnn_ring(int nqbits);
value* make_grid(int nrows, int ncols);
value* trivial_layout(int nqbits);
value* list_to_layout(int nqbits, int* buff);
void layout_to_list(value* layout, int nqbits, int* buff);
