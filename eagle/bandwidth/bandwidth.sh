#!/bin/bash
me=$1
binary=$2
hostfile=$3
bw=$4

hoststring=$( cat $hostfile )
IFS=$'\n' hosts=($hoststring)

bwstring=""

for i in "${hosts[@]}"
do
    printf "$me $i " 
    bwstring=$bwstring"$me $i " 
    out=$( timeout 20 mpiexec -hosts $me,$i -n 2 $binary 2> /dev/null )
    status=$?
    if [ $status != '0' ]
    then
        bwstring=$bwstring"0"$'\n' 
        echo 0
    else
        bwstring=$bwstring"$out"$'\n' 
        echo $out
    fi
done
echo "$bwstring" > $bw