# pyvoqc

This repository provides a Python wrapper around the VOQC quantum circuit compiler.

VOQC is a **verified optimizer for quantum circuits**, implemented and *formally verified* in the [Coq proof assistant](https://coq.inria.fr/). All VOQC optimizations are *guaranteed* to preserve the semantics of the original circuit, meaning that any optimized circuit produced by VOQC has the same behavior as the input circuit. VOQC was presented as a [distinguished paper at POPL 2021](https://arxiv.org/abs/1912.02250). Coq code and proofs are available at [github.com/inQWIRE/SQIR](https://github.com/inQWIRE/SQIR) and the extracted OCaml code (which the Python wraps) is available at [github.com/inQWIRE/mlvoqc](https://github.com/inQWIRE/mlvoqc)

To run VOQC, we (1) extract the verified Coq code to OCaml, (2) compile the extracted OCaml code to a library, (3) wrap the OCaml library in C, and (4) provide a Python interface for the C wrapper.

## Table of Contents

- [pyvoqc](#pyvoqc)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
  - [Installation](#installation)
  - [Tutorial](#tutorial)
  - [Directory Contents](#directory-contents)
  - [API](#api)
  - [Acknowledgements](#acknowledgements)

## Setup

pyvoqc requires Python 3 and a compatible version of pip. We recommend using [Anaconda](https://www.anaconda.com/products/individual) to make sure you get the right versions (e.g., see the instructions for setting up a Qiskit environment [here](https://qiskit.org/documentation/getting_started.html))

Although pyvoqc is a Python package, it requires OCaml to build the underlying library code. At some point in the future we will remove this dependency by pre-compiling binaries, but for now you will need to install [opam](https://opam.ocaml.org/doc/Install.html). Once you have opam installed, follow the instructions below to set up your environment.
```
# environment setup
opam init
eval $(opam env)

# install the OCaml version of VOQC
opam pin voqc https://github.com/inQWIRE/mlvoqc.git#mapping
```
*Note*: If you have previously installed `voqc` with opam, run `opam uninstall voqc` first to ensure that you get the right version.

## Installation

After installing voqc through opam (following the instructions under [Setup](#setup) above), run `./install.sh`. This will build the VOQC library using dune and then "install" our Python package with pip.

*Notes:*
* If you are building the voqc library on a Mac, you will likely see the warning `ld: warning: directory not found for option '-L/opt/local/lib'`. This is due to zarith (see [ocaml/opam-repository#3000](https://github.com/ocaml/opam-repository/issues/3000)) and seems to be fine to ignore.

To check that installation worked, open a Python shell and try `from pyvoqc.voqc import VOQCCircuit`.

## Tutorial

The tutorial requires JuPyter and Qiskit (`pip install jupyter qiskit`). 

To run the tutorial locally, run `jupyter notebook` on the command line from the pyvoqc directory and open http://localhost:8888/notebooks/tutorial.ipynb. 

You should also be able to view the tutorial on GitHub, but if that fails then go to https://nbviewer.jupyter.org/github/inQWIRE/pyvoqc/blob/main/tutorial.ipynb.

## Directory Contents

* `lib` contains code for building a C libary that wraps around the OCaml VOQC package.
* `pyvoqc/` contains the Python wrapper code.
* `tutorial_files/` contains files for the pyvoqc tutorial.

## API

VOQC currently supports the OpenQASM 2.0 file format, excluding measurement, and the following gates:
* i, x, y, z
* h
* s, sdg
* t, tdg
* rx(f), ry(f), rz(f)
* u1(f)
* u2(f,f)
* u3(f,f,f)
* cx
* cz
* swap
* ccx
* ccz

Above, "f" is a float expression (possibly including the constant pi) and "i" is an integer expression.

We recommend using our Qiskit pass manager to perform VOQC verified optimization and validated mapping (as in the tutorial). 
However, it is also possibly to call `pyvoqc` functions directly. 
Here are the functions exposed by our interface:
* `get_library_handle`
* `VOQCCircuit(lib,fname)`
* `print_info`
* `write`
* `count_gates`
* `count_clifford_rzq`
* `total_gate_count`
* `check_well_typed`
* `convert_to_rzq`
* `convert_to_ibm`
* `decompose_to_cnot`
* `replace_rzq`
* `optimize_ibm`
* `not_propagation`
* `hadamard_reduction`
* `cancel_single_qubit_gates`
* `cancel_two_qubit_gates`
* `merge_rotations`
* `optimize_nam`
* `optimize`
* `decompose_swaps`
* `trivial_layout`
* `list_to_layout`
* `c_graph_from_coupling_map`
* `check_swap_equivalence`
* `check_constraints`
There are descriptions of some of these functions in our tutorial. Otherwise, you can use the [documentation for our OCaml library](https://inqwire.github.io/mlvoqc/voqc/Voqc/index.html) for reference.

## Acknowledgements

This project is supported by the U.S. Department of Energy, Office of Science, Office of Advanced Scientific Computing Research, Quantum Testbed Pathfinder Program under Award Number DE-SC0019040 and the Air Force Office of Scientific Research under Grant Number FA95502110051.