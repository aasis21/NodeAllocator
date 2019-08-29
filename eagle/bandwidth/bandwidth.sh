#!/bin/bash
me=$1
binary=$2
hostfile=$3
hoststring=$( cat $hostfile )
IFS=$'\n' hosts=($hoststring)

for i in "${hosts[@]}"
do
    printf "$me $i " : 
    out=$( timeout 10 mpiexec -hosts $me,$i -n 2 $binary 2> /dev/null )
    status=$?
    if [ $status != '0' ]
    then
        echo 0
    else
        echo $out
    fi
done
