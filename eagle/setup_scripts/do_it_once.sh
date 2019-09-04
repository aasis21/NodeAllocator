#!/bin/bash
for id in {1..50}
do  
    echo "ssh into csews$id"
    ssh -q -o ConnectTimeout=2 csews$id exit
done
