#!/bin/bash
for id in {1..25}
do  
    # echo "ssh into csews$id for launching daemons"
    ssh -q -o ConnectTimeout=2 csews$id ~/UGP/eagle/monitor/localDaemonStatus.sh
done
