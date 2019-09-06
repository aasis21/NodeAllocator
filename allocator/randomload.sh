#!/bin/bash
binary=$1
while :
do
    > randomload_out.tmp
    numhosts=`shuf -i 6-16 -n 1`
    ppn=4
    proc_count=$(($ppn*$numhosts))
    echo "Num hosts: $numhosts | ppn : $ppn | proc_count : $proc_count"
    cat /users/btech/akashish/.eagle/livehosts.txt | sort -R | sort -R | head -n $numhosts > loadhosts
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
        mpiexec -n $proc_count -ppn $ppn -hostfile loadhosts $binary >> randomload_out.tmp
    fi
    end=`date +%s`
    runtime=$((end-start))
    echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    echo "MPI PROGRAM ENDS : $end :: Total Time : $runtime"
    echo "======================================================================"
done