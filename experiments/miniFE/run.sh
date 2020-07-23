#!/bin/bash
array="${@}"
proc_count=$1
ppn=$2
binary=${array[@]:4}
echo $binary


echo "" > miniamr.log

echo "" >> metadata.log
echo "" >> metadata.log
echo "======================================================================" >> metadata.log
echo "proc count : $proc_count BINARY : $binary" >> metadata.log
echo "======================================================================" >> metadata.log
echo "======================================================================" >> metadata.log

~/UGP/allocator/src/allocator_improved.out $proc_count $ppn >> metadata.log

echo ""
#echo "Selected Improved Algo hosts are"
#cat hostsimproved
## echo "======================================================================"
#start=`date +%s%3N`
## echo "MPI PROGRAM STARTS : $start "
## echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#if (( $ppn == 0 ))
#then
#   mpiexec -n $proc_count -hostfile hostsimproved $binary >> miniamr.log
#else
#    mpiexec -n $proc_count -ppn $ppn -hostfile hostsimproved $binary >> miniamr.log
#fi
#end=`date +%s%3N`
#runtime=$((end-start))
## echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#echo "MPI PROGRAM :: Total Time : $runtime"
## echo "======================================================================"
#

echo ""
echo "Selected Algo hosts are"
cat hosts
# echo "======================================================================"
start=`date +%s%3N`
# echo "MPI PROGRAM STARTS : $start "
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
if (( $ppn == 0 ))
then
   mpiexec -n $proc_count -hostfile hosts $binary >> miniamr.log
else
    mpiexec -n $proc_count -ppn $ppn -hostfile hosts $binary >> miniamr.log
fi
end=`date +%s%3N`
runtime=$((end-start))
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM :: Total Time : $runtime"
# echo "======================================================================"

echo ""
echo "Selected min compute load hosts are"
cat comphosts
# echo "======================================================================"
start=`date +%s%3N`
# echo "MPI PROGRAM STARTS WITT MAX COMPUTES: $start "
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
if (( $ppn == 0 ))
then
   mpiexec -n $proc_count -hostfile comphosts $binary >> miniamr.log
else
    mpiexec -n $proc_count -ppn $ppn -hostfile comphosts $binary >> miniamr.log
fi
end=`date +%s%3N`
runtime=$((end-start))
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM MIN COMPUTE LOAD :: Total Time : $runtime"
# echo "======================================================================"



numhosts=`wc -l < hosts`
cat ~/.eagle/livehosts.txt | sort -R | head -n $numhosts > randomhosts && sed -e 's/$/:4/' -i randomhosts
echo ""
echo "Randomly Selected hosts are"
cat randomhosts
# echo "======================================================================"
start=`date +%s%3N`
# echo "MPI PROGRAM STARTS ON RANDOM : $start "
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
if (( $ppn == 0 ))
then
   mpiexec -n $proc_count -hostfile randomhosts $binary >> miniamr.log
else
    mpiexec -n $proc_count -ppn $ppn -hostfile randomhosts $binary >> miniamr.log
fi
end=`date +%s%3N`
runtime=$((end-start))
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM RANDOM :: Total Time : $runtime"
# echo "======================================================================"

numlivehosts=`wc -l < ~/.eagle/livehosts.txt`	
selectedend=`shuf -i $numhosts-$numlivehosts -n 1`	
cat ~/.eagle/livehosts.txt | head -n $selectedend | tail -n $numhosts > sequencehosts && sed -e 's/$/:4/' -i sequencehosts	
echo ""	

echo "Random sequence Selected hosts are"
cat sequencehosts
# echo "======================================================================"	
start=`date +%s%3N`	
# echo "MPI PROGRAM STARTS ON SEQUENCE : $start "	
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"	
if (( $ppn == 0 ))	
then	
   mpiexec -n $proc_count -hostfile sequencehosts $binary >> miniamr.log	
else	
    mpiexec -n $proc_count -ppn $ppn -hostfile sequencehosts $binary  >> miniamr.log
fi	
end=`date +%s%3N`
runtime=$((end-start))
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"	
echo "MPI PROGRAM Sequence  :: Total Time : $runtime"
# echo "======================================================================"
