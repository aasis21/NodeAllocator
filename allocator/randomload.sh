#!/bin/bash
numhosts=$1
ppn=$2
proc_count=$3
binary=$4
cat ~/.eagle/livehosts.txt | sort -R | sort -R | head -n $numhosts > loadhosts
echo ""
echo ""
echo "Randomly Selected hosts for dummy load"
cat loadhosts
echo "======================================================================"
start=`date +%s`
echo "MPI PROGRAM STARTS FOR RANDOM DUMMY LOAD : $start "
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
if (( $ppn == 0 ))
then
   mpiexec -n $proc_count -hostfile loadhosts $binary
else
    mpiexec -n $proc_count -ppn $ppn -hostfile loadhosts $binary
fi
end=`date +%s`
runtime=$((end-start))
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM ENDS : $end :: Total Time : $runtime"
echo "======================================================================"

