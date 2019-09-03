#!/bin/bash
me=$1
binary=$2
hostfile=$3
latency=$4

hoststring=$( cat $hostfile )
IFS=$'\n' hosts=($hoststring)

latencystring=""

for i in "${hosts[@]}"
do
    printf "$me $i " 
    latencystring=$latencystring"$me $i " 
    out=$( timeout 5 mpiexec -hosts $me,$i -n 2 $binary 2> /dev/null )
    status=$?
    if [ $status != '0' ]
    then
        latencystring=$latencystring"3000"$'\n' 
        echo 1000000
    else
        latencystring=$latencystring"$out"$'\n' 
        echo $out
    fi
done
