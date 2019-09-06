#!/bin/bash
for id in {80..90}
do  
    echo "ssh into csews$id"
    ssh -q -o ConnectTimeout=2 csews$id exit
done
for id in {50..60}
do  
    echo "ssh into csews$id"
    ssh -q -o ConnectTimeout=2 csews$id exit
done