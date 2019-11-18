#!/bin/bash

hostfile=$1
hoststring=$( cat $hostfile )
IFS=$'\n' hosts=($hoststring)

for i in "${hosts[@]}"
do
    if [[ $i = \#* ]]
    then
        :
    else
        ssh -q -o ConnectTimeout=2 $i ~/UGP/eagle/monitor/localDaemonStatus.sh
    fi
done