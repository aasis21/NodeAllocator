#!/bin/bash
command=$1
echo "latency on $HOSTNAME" 
python3 ~/UGP/eagle/latency/latencyd.py $command $HOSTNAME 2> /dev/null
echo "bw on $HOSTNAME"
python3 ~/UGP/eagle/bandwidth/bandwidthd.py $command $HOSTNAME 2> /dev/null
echo "eagle on $HOSTNAME"
#python3 ~/UGP/eagle/eagle.py $command $HOSTNAME 2> /dev/null
