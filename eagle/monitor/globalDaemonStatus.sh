#!/bin/bash

hostfile=$1
hoststring=$( cat $hostfile )
IFS=$'\n' hosts=($hoststring)
monitor="Monitord :: "
livehost="LiveHostsd :: "
bwd="bwd :: "
ltd="ltd :: "

for i in "${hosts[@]}"
do
    if [[ $i = \#* ]]
    then
        :
    else
        status=$(ssh -q -o ConnectTimeout=2 $i ~/UGP/eagle/monitor/localDaemonStatus.sh)
        if [ "$status" = "" ]
        then 
            printf ""
        else
            echo $(echo $status | cut -d ":" -f 1) :: nodeInfoD ::  $(echo $status | cut -d ":" -f 5)
            name=$(echo $status | cut -d ":" -f 1)
            s_lt=$(echo $status | cut -d ":" -f 8 | xargs)
            s_bwd=$(echo $status | cut -d ":" -f 11 | xargs)
            s_live=$(echo $status | cut -d ":" -f 14 | xargs)
            s_monitor=$(echo $status | cut -d ":" -f 17 | xargs)
            if [ "$s_monitor" = "up" ]; 
            then
                monitor="$monitor :: $name"
            fi

            if [ "$s_lt" = "up" ]; 
            then
                ltd="$ltd :: $name"
            fi

            if [ "$s_bwd" = "up" ]; 
            then
                bwd="$bwd :: $name"
            fi

            if [ "$s_live" = "up" ]; 
            then
                livehost="$livehost :: $name"
            fi
        fi
    fi
done
echo " "
echo $monitor
echo $livehost
echo $ltd
cat ~/.eagle/bw.txt.stamp
echo $bwd
cat ~/.eagle/lt.txt.stamp
