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
int total_gate_count(value* circ);
value* decompose_to_cnot(value* circ);
value* replace_rzq(value* circ);

// Optimization
value* optimize_nam(value* circ);
value* optimize_ibm(value* circ);

// Mapping
int check_layout(value* layout, int nqbits);
CircLayoutPair simple_map(value* circ, value* layout, value* c_graph);
value* make_tenerife();
value* trivial_layout(int nqbits);
value* list_to_layout(int nqbits, int* buff);
void layout_to_list(value* layout, int nqbits, int* buff);
