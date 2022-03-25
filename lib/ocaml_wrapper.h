#include <caml/mlvalues.h>

void init();
void destroy(value*);

typedef struct circ_int_pair
{
  value* circ;
  int nqbits;
} CircIntPair ;

typedef struct int_int_pair
{
  int x;
  int y;
} IntIntPair ;

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
int count_total(value* circ);
int count_rzq_clifford(value* circ);
int check_well_typed(value* circ, int nqbits);
value* convert_to_rzq(value* circ);
value* convert_to_ibm(value* circ);
value* decompose_to_cnot(value* circ);
value* replace_rzq(value* circ);

// Optimization
value* optimize_ibm(value* circ);
value* not_propagation(value* circ);
value* hadamard_reduction(value* circ);
value* cancel_single_qubit_gates(value* circ);
value* cancel_two_qubit_gates(value* circ);
value* merge_rotations(value* circ);
value* optimize_nam(value* circ);
value* optimize(value* circ);

// Mapping
value* decompose_swaps(value* circ, value* c_graph);
value* trivial_layout(int nqbits);
int check_list(int nqbits, int* buff);
value* list_to_layout(int nqbits, int* buff);
value* c_graph_from_coupling_map(int nqbits, int len, IntIntPair* coupling_map);
int check_swap_equivalence(value* circ1, value* circ2, value* layout1, value* layout2);
int check_constraints(value* circ, value* c_graph);