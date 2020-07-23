#!/bin/bash
echo "" > log
for iter in {1..8}
do
for n in 8 16 32 64
do
	for s in 8 16 24 32 40
	do
		echo "++++++++++++++++++++++++++++++++++++ iter = $iter  n = $n ++++ s = $s +++++++++++++++++++++++++++++++++++++" | tee -a log
		~/UGP/allocator/src/allocator_improved.out $n 4 >> m 
		mpiexec -n $n -hostfile hosts ./miniMD -s $s | tail -30 | head -16 | tee -a log
	       	cat hosts | tee -a log	
	done
done
done

