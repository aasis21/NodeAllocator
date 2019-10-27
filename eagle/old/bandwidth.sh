#!/bin/bash
me=$1
binary=$2
hostfile=$3
bw=$4
echo "" > $bw.tmpp
hoststring=$( cat $hostfile | tail -n+`grep  -n "^$me$" $hostfile  | cut -f1 -d:` 2> /dev/null )

IFS=$'\n' hosts=($hoststring)

for i in "${hosts[@]}"
do
    printf "$me $i " 
    printf "$me $i "  >> $bw.tmpp
    out=$( timeout 250 mpiexec -hosts $me,$i -n 2 $binary 2> /dev/null )
    status=$?
    if [ $status != '0' ]
    then
        echo 0
        echo 0 >> $bw.tmpp
    else
        bwstring=$bwstring"$out"$'\n' 
        echo $out >> $bw.tmpp
        echo $out
    fi
done


hoststring=$( cat $hostfile | head -n `grep  -n "^$me$" $hostfile  | cut -f1 -d:` 2> /dev/null )

IFS=$'\n' hosts=($hoststring)

for i in "${hosts[@]}"
do
    printf "$me $i " 
    printf "$me $i "  >> $bw.tmpp
    out=$( timeout 250 mpiexec -hosts $me,$i -n 2 $binary 2> /dev/null )
    status=$?
    if [ $status != '0' ]
    then
        echo 0
        echo 0 >> $bw.tmpp
    else
        bwstring=$bwstring"$out"$'\n' 
        echo $out >> $bw.tmpp
        echo $out
    fi
done
