# VOQC Interoperability

## Overview

This README contains instructions for using the VOQC optimizer with widely used quantum frameworks.

VOQC is currently compatible with the following frameworks:
* Cirq (Version 0.8.2)
* Qiskit (Version 0.19.6)

## Using VOQC Transpiler Pass in Qiskit

To pass a qiskit circuit to the VOQC optimizer, append `VOQC([list of optimizations])` to a pass manager. The argument `list of optimizations` is an optional argument that allows custom optimizations to be run. Appending `VOQC()` to a pass manager without a list will run the main optimize function in VOQC. The client file must be run from the VOQC directory.

*Example*: The following is a transpiler pass to VOQC using a circuit built in qiskit. 
```
from qiskit.transpiler import PassManager
from wrapper.qiskit.voqc_optimization import QisVOQC
from qiskit import QuantumCircuit

#Build Quantum Circuit
circ = QuantumCircuit(2)
circ.cx(0, 1)
circ.cx(0, 1)
circ.h(0)

#Pass to VOQC
pm = PassManager()
#Call cancel_two_qubit_gates
pm.append(QisVOQC(["cancel_two_qubit_gates"]))
new_circ = pm.run(circ)
```

## Using VOQC optimization pass in Cirq

**TODO**
