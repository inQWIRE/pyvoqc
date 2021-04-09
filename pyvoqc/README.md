# VOQC Interoperability

## Overview

This README contains instructions for using the VOQC optimizer with widely used quantum frameworks.

VOQC is currently compatible with the following frameworks:
* Cirq (Version 0.8.2)
* Qiskit (Version 0.19.6)

## Using VOQC Transpiler Pass in Qiskit

To pass a qiskit circuit to the VOQC optimizer, append `QisVOQC([list of optimizations])` to a pass manager. The argument `list of optimizations` is an optional argument that allows custom optimizations to be run. Appending `VOQC()` to a pass manager without a list will run the main optimize function in VOQC. The client file must be run from the `pyvoqc` directory.

*Example*: The following is a transpiler pass to VOQC using a circuit built in qiskit. 
```
from qiskit.transpiler import PassManager
from pyvoqc.qiskit.voqc_pass import QiskitVOQC
from qiskit import QuantumCircuit

# build quantum circuit
circ = QuantumCircuit(2)
circ.cx(0, 1)
circ.cx(0, 1)
circ.h(0)

#Pass to VOQC
pm = PassManager()
#Call cancel_two_qubit_gates
pm.append(QiskitVOQC(["optimize_nam"]))
new_circ = pm.run(circ)
```

## Using VOQC Optimization Pass in Cirq

Passing a Cirq circuit object to the VOQC compiler pass is similar to the built-in optimizations. Just like the built-in Cirq optimizations, VOQC implements the `optimize_circuit(input_circ)` function. To call this non-static method, create an instance of `CqVOQC` with an optional argument `list of optimizations` and call the `optimize_circuit(input_cirq)` function with `input_cirq` being the circuit to be optimized. The `list of optimizations` argument is identical to that of Qiskit as it is a list that allows the execution of customized optimizations. Again, the client file must be run from the pyvoqc directory. 

*Example*: The following is a compiler pass to VOQC using a circuit built in Cirq. 
```
import cirq
from pyvoqc.cirq.voqc_optimization import CqVOQC

#Build Circuit Object
q_0 = cirq.NamedQubit("q_0")
q_1 = cirq.NamedQubit("q_1")
circ = cirq.Circuit([cirq.CNOT.on(q_0,q_1), cirq.CNOT.on(q_0, q_1), cirq.H.on(q_0)])

#Instantiate CqVOQC compiler pass and pass our sample circuit 'circ' with the "optimize_circuit" function
pass_object = CqVOQC(["cancel_two_qubit_gates"])
new_circ = pass_object.optimize_circuit(circ)

"""
The previous two lines could also be combined:

new_circ = CqVOQC(["cancel_two_qubit_gates"]).optimize_circuit(circ)

"""
```
