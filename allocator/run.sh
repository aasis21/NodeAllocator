#!/bin/bash
proc_count=$1
binary=$3
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
   mpiexec -n $proc_count -hostfile hosts $binary >> out.tmp
else
    mpiexec -n $proc_count -ppn $ppn -hostfile hosts $binary >> out.tmp
fi
end=`date +%s`
runtime=$((end-start))
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM ENDS : $end :: Total Time : $runtime"
echo "======================================================================"


numhosts=`wc -l < hosts`
numlivehosts=`wc -l < /users/btech/akashish/.eagle/livehosts.txt`
selectedend=`shuf -i $numhosts-$numlivehosts -n 1`
cat /users/btech/akashish/.eagle/livehosts.txt | head -n $selectedend | tail -n $numhosts > sequencehosts
echo ""
echo ""
echo "Random sequence Selected hosts are"
cat sequencehosts
echo "======================================================================"
start=`date +%s`
echo "MPI PROGRAM STARTS ON SEQUENCE : $start "
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
if (( $ppn == 0 ))
then
   mpiexec -n $proc_count -hostfile sequencehosts $binary >> out.tmp
else
    mpiexec -n $proc_count -ppn $ppn -hostfile sequencehosts $binary  >> out.tmp
fi
end=`date +%s`
runtime=$((end-start))
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM ENDS : $end :: Total Time : $runtime"
echo "======================================================================"


numhosts=`wc -l < hosts`
cat ~/.eagle/livehosts.txt | sort -R | sort -R | head -n $numhosts > randomhosts
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
   mpiexec -n $proc_count -hostfile randomhosts $binary >> out.tmp
else
    mpiexec -n $proc_count -ppn $ppn -hostfile randomhosts $binary >> out.tmp
fi
end=`date +%s`
runtime=$((end-start))
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM ENDS : $end :: Total Time : $runtime"
echo "======================================================================"

