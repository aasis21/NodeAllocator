#!/bin/bash
proc_count=$1
binary=$2
ppn=$3
./src/min_diameter.out $proc_count $ppn | tee -a output.tmp
echo "Selected hosts are"
cat hosts
mpiexec -n $proc_count -ppn $ppn -hostfile hosts $binary