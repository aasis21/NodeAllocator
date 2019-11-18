#!/bin/bash
binary=$1
dummyloadnum=$2
while :
do
    numhosts=`shuf -i 4-9 -n 1`
    ppn=3
    proc_count=$(($ppn*$numhosts))
    echo "Num hosts: $numhosts | ppn : $ppn | proc_count : $proc_count"
    cat /users/btech/akashish/.eagle/livehosts.txt | sort -R | sort -R | head -n $numhosts > loadhosts.txt
    echo ""
    echo ""
    echo "Randomly Selected hosts for dummy load"
    cat loadhosts.txt
    echo "======================================================================"
    start=`date +%s`
    echo "MPI PROGRAM STARTS FOR RANDOM DUMMY LOAD : $start "
    echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    mpiexec -n $proc_count -ppn $ppn -hostfile loadhosts.txt $binary > /dev/null

    end=`date +%s`
    runtime=$((end-start))
    echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    echo "MPI PROGRAM ENDS : $end :: Total Time : $runtime"
    echo "======================================================================"
done
