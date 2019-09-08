#!/bin/bash
me=$1
binary=$2
tphosts=$3
printf "" > $tphosts
touch $tphosts.tmp
for i in {1..60}
do
    echo "csews$i" >> $tphosts
done
hoststring=$( cat $tphosts | sort -R )
IFS=$'\n' hosts=($hoststring)
for i in "${hosts[@]}"
do
    printf "$me $i " 
    printf "$me $i "  >> $tphosts.tmp
    out=$( timeout 5 mpiexec -hosts $me,$i -n 2 $binary 2> /dev/null  )
    status=$?
    if [ $status != '0' ]
    then
        echo 50000
        echo 50000 >> $tphosts.tmp
    else
        echo $out
        echo $out >> $tphosts.tmp
    fi
done
