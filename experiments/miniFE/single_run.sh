#!/bin/bash
rm *yaml
~/UGP/allocator/src/allocator_improved.out $4 2 >> m
mpiexec -n $4 -hostfile hosts ./miniFE.x -nx $1 -ny $2 -nz $3
cat hosts
cat *yaml | tail -5

