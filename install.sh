#!/bin/bash

echo "dune build lib/libvoqc.so"
dune build lib/libvoqc.so
echo "" # idk why dune doesn't print a newline -KH
echo "pip install ."
pip install .
echo "cp _build/default/lib/libvoqc.so pyvoqc/lib/"
mkdir -p pyvoqc/lib
cp _build/default/lib/libvoqc.so pyvoqc/lib/