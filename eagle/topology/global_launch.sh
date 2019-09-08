#!/bin/bash
for id in {1..60}
do  
    # echo "ssh into csews$id for launching daemons"
    ssh -q -o ConnectTimeout=2 csews$id python3 ~/UGP/eagle/topology/tpd.py $1 #2> /dev/null
done
