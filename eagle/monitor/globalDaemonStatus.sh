#!/bin/bash
for id in {1..34}
do  
    # echo "ssh into csews$id for launching daemons"
    ssh -q -o ConnectTimeout=2 csews$id ~/UGP/eagle/monitor/localDaemonStatus.sh
done

for id in {50..55}
do  
    # echo "ssh into csews$id for launching daemons"
    ssh -q -o ConnectTimeout=2 csews$id ~/UGP/eagle/monitor/localDaemonStatus.sh
done

# for id in {80..90}
# do  
#     # echo "ssh into csews$id for launching daemons"
#     ssh -q -o ConnectTimeout=2 csews$id ~/UGP/eagle/monitor/localDaemonStatus.sh
# done