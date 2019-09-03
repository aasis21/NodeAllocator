#!/bin/bash
for id in {1..50}
do  
    echo "ssh into csews$id for launching daemons"
    ssh -q -o ConnectTimeout=2 csews$id ~/UGP/eagle/launcher.sh $1
    echo " "
    echo " "
done
