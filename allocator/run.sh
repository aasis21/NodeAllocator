#!/bin/bash
proc_count=$1
binary=$2
ppn=$3
./src/min_diameter.out $proc_count $ppn 
echo ""
echo "Selected hosts are"
cat hosts

echo "======================================================================"
start=`date +%s`
echo "MPI PROGRAM STARTS : $start "
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
if (( $ppn == 0 ))
then
   mpiexec -n $proc_count -hostfile hosts $binary
else
    mpiexec -n $proc_count -ppn $ppn -hostfile hosts $binary
fi
end=`date +%s`
runtime=$((end-start))
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM ENDS : $end :: Total Time : $runtime"
echo "======================================================================"



