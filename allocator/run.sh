#!/bin/bash
array="${@}"
proc_count=$1
binary=${array[@]:3}
echo $binary
ppn=$2
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

numhosts=`wc -l < hosts`
cat ~/.eagle/livehosts.txt | sort -R | head -n $numhosts > randomhosts
echo ""
echo ""
echo "Randomly Selected hosts are"
cat randomhosts
echo "======================================================================"
start=`date +%s`
echo "MPI PROGRAM STARTS ON RANDOM : $start "
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
if (( $ppn == 0 ))
then
   mpiexec -n $proc_count -hostfile randomhosts $binary
else
    mpiexec -n $proc_count -ppn $ppn -hostfile randomhosts $binary
fi
end=`date +%s`
runtime=$((end-start))
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM ENDS : $end :: Total Time : $runtime"
echo "======================================================================"
