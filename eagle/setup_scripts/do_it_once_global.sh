#!/bin/bash
# for id in {1..50}
# do  
#     echo "ssh into csews$id for do_it_once"
#     ssh -q -o ConnectTimeout=2 csews$id ~/UGP/eagle/do_it_once.sh
# done
for id in {1..60}
do  
    echo "ssh into csews$id for do_it_once"
    ssh -q -o ConnectTimeout=2 csews$id uptime
done
