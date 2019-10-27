#!/bin/bash
hostfile=$1
livehosts=$2
tmp=$3

printf "" > $tmp
hoststring=$( cat $hostfile )
IFS=$'\n' hosts=($hoststring)

for i in "${hosts[@]}"
do
    if [[ $i = \#* ]]
    then
        :
    else
        ssh -q -o ConnectTimeout=2 $i exit 
        status=$?
        echo $i $status
        if [ $status == '0' ]
        then
            echo $i >> $tmp
        fi
    fi
done

date > $livehosts.stamp
mv $tmp $livehosts 