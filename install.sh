#!/bin/bash

echo "dune build lib/libvoqc.so"
dune build lib/libvoqc.so
echo "pip install ."
pip install .
echo "cp _build/default/lib/libvoqc.so pyvoqc/lib"
cp _build/default/lib/libvoqc.so pyvoqc/lib