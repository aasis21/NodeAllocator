#!/bin/bash
array="${@}"
proc_count=$1
ppn=$2
binary=${array[@]:4}
echo $binary

touch metadata.log

echo "" >> metadata.log
echo "" >> metadata.log
echo "======================================================================" >> metadata.log
echo "proc count : $proc_count BINARY : $binary" >> metadata.log
echo "======================================================================" >> metadata.log
echo "======================================================================" >> metadata.log

~/UGP/allocator/src/allocator_improved.out $proc_count $ppn >> metadata.log


echo ""
echo "Selected Improved Algo hosts are"
cat hostsimproved
# echo "======================================================================"
start=`date +%s%3N`
# echo "MPI PROGRAM STARTS : $start "
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

mpiexec -n $n -hostfile hostsimproved ./miniMD | tail -30 | head -16 | tee -a log 

end=`date +%s%3N`
runtime=$((end-start))
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM :: Total Time : $runtime"
# echo "======================================================================"


echo ""
echo "Selected Algo hosts are"
cat hosts
# echo "======================================================================"
start=`date +%s%3N`
# echo "MPI PROGRAM STARTS : $start "
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
mpiexec -n $n -hostfile hosts ./miniMD | tail -30 | head -16 | tee -a log 

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
mpiexec -n $n -hostfile comphosts ./miniMD | tail -30 | head -16 | tee -a log 

end=`date +%s%3N`
runtime=$((end-start))
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM MIN COMPUTE LOAD :: Total Time : $runtime"
# echo "======================================================================"



numhosts=`wc -l < hosts`
cat ~/.eagle/livehosts.txt | sort -R | head -n $numhosts > randomhosts  
echo ""
echo "Randomly Selected hosts are"
cat randomhosts
# echo "======================================================================"
start=`date +%s%3N`
# echo "MPI PROGRAM STARTS ON RANDOM : $start "
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
mpiexec -n $n -hostfile randomhosts ./miniMD | tail -30 | head -16 | tee -a log 

end=`date +%s%3N`
runtime=$((end-start))
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "MPI PROGRAM RANDOM :: Total Time : $runtime"
# echo "======================================================================"

numlivehosts=`wc -l < /users/btech/akashish/.eagle/livehosts.txt`	
selectedend=`shuf -i $numhosts-$numlivehosts -n 1`	
cat /users/btech/akashish/.eagle/livehosts.txt | head -n $selectedend | tail -n $numhosts > sequencehosts	
echo ""	

echo "Random sequence Selected hosts are"
cat sequencehosts
# echo "======================================================================"	
start=`date +%s%3N`	
# echo "MPI PROGRAM STARTS ON SEQUENCE : $start "	
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"	
mpiexec -n $n -hostfile sequencehosts ./miniMD | tail -30 | head -16 | tee -a log 
end=`date +%s%3N`
runtime=$((end-start))
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"	
echo "MPI PROGRAM Sequence  :: Total Time : $runtime"
# echo "======================================================================"