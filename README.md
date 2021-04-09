# pyvoqc

This repository provides a Python wrapper around the VOQC quantum circuit compiler.

VOQC is a **verified optimizer for quantum circuits**, implemented and *formally verified* in the [Coq proof assistant](https://coq.inria.fr/). All VOQC optimizations are *guaranteed* to preserve the semantics of the original circuit, meaning that any optimized circuit produced by VOQC has the same behavior as the input circuit. VOQC was presented as a [distinguished paper at POPL 2021](https://arxiv.org/abs/1912.02250). Coq code and proofs are available at [github.com/inQWIRE/SQIR](https://github.com/inQWIRE/SQIR) and the extraced OCaml code (which the Python wraps) is available at [github.com/inQWIRE/mlvoqc](https://github.com/inQWIRE/mlvoqc)

To run VOQC, we (1) extract the verified Coq code to OCaml, (2) compile the extracted OCaml code to a library, (3) wrap the OCaml library in C, and (4) provide a Python interface for the C wrapper.

### Setup

Although pyvoqc is a Python package, it requires OCaml to build the underlying library code. At some point in the future we will remove this dependency by pre-compiling binaries, but for now you will need to install [opam](https://opam.ocaml.org/doc/Install.html). Once you have opam installed, follow the instructions below to set up your environment.
```
# environment setup
opam init
eval $(opam env)

# install some version of the OCaml compiler in a switch named "voqc"
opam switch create voqc 4.10.0
eval $(opam env)

# install voqc (current supported version is 0.2.0)
opam install voqc.0.2.0
```

*Notes*:
* Depending on your system, you may need to replace 4.10.0 in the instructions above with something like "ocaml-base-compiler.4.10.0". Opam error messages and warnings are typically informative, so if you run into trouble then make sure you read the console output.

### Installation

After installing voqc through opam (following the instructions in setup above), run `./install.sh`. This will build the VOQC library using dune and then "install" our Python package with pip.

*Notes:*
* If you are building the voqc library on a Mac, you will likely see the warning `ld: warning: directory not found for option '-L/opt/local/lib'`. This is due to zarith (see [ocaml/opam-repository#3000](https://github.com/ocaml/opam-repository/issues/3000)) and seems to be fine to ignore.

## Running VOQC

Dependencies:
  * Python 3
  * JuPyter and Qiskit (for the tutorial, `pip3 install jupyter qiskit`)

The voqc.py file in the wrapper/ directory provides a simple wrapper around the VOQC library functions. Here is a minimal example of how to use it:
```
from pyvoqc.voqc import VOQC

# load circuit
c = VOQC("tutorial-files/tof_3_example.qasm")

# run a single optimization (in this case, 1q gate cancellation)
c.cancel_single_qubit_gates()

# print current gate counts
c.print_info()

# run all optimizations
c.optimize()

# write the optimized file
c.write("out.qasm")
```

We also provide support for running VOQC as a pass in Qiskit's PassManager. You can find the details in our [tutorial](tutorial.ipynb). You *should* be able to view our tutorial on GitHub, but if this fails then go to https://nbviewer.jupyter.org/ and copy the link https://github.com/inQWIRE/pyvoqc/blob/main/tutorial.ipynb when prompted. To run the tutorial locally, run `jupyter notebook` on the command line from the pyvoqc directory and open http://localhost:8888/notebooks/tutorial.ipynb.

## Directory Contents

* `lib` contains code for building a VOQC C libary.
* `lib/ml` contains (1)  OCaml code extracted from our verified Coq definitions and (2) hand-written OCaml harness code. This code is all from the [SQIR](https://github.com/inQWIRE/SQIR) repository and SHOULD NOT be edited from the pyvoqc directory. We will periodically update code in the `lib/ml` directory to be consistent with the current Coq development.
* `wrapper/` contains the Python wrapper code.
* `tutorial_files/` contains files for the pyvoqc tutorial.

## API

VOQC currently supports the OpenQASM 2.0 file format, excluding measurement, and the following gates:
* t, tdg
* s, sdg
* z
* rzq(num,den) where num and den are integer expressions
* rz(f) where f is a float expression, possibly including the constant pi
* h
* x
* cx
* ccx
* ccz

rzq is a non-standard gate that we have defined specifically for VOQC. rzq(num,den) performs a rotation about the z-axis by ((num /den) * pi) for integers num and den. We have defined the gate this way to avoid floating point numbers, which significantly complicate verification. Gates of the form rz(f) are automatically converted into our rzq form by dividing the float f by pi and converting the result to its rational representation.

The following functions are exposed by our Python interface:
* `VOQC(fname)` VOQC class constructor, takes an OpenQASM filename as input
* `not_propagation` 
* `hadamard_reduction`
* `cancel_single_qubit_gates`
* `cancel_two_qubit_gates`
* `merge_rotations`
* `optimize` Applies all the optimizations above in a pre-determined order
* `print_info`
* `write`

## Acknowledgements

This project is supported by the U.S. Department of Energy, Office of Science, Office of Advanced Scientific Computing Research, Quantum Testbed Pathfinder Program under Award Number DE-SC0019040.
