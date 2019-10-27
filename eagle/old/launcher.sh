#!/bin/bash
command=$1
echo "latency on $HOSTNAME" 
python3 ~/UGP/eagle/latency/latencyd.py $command $HOSTNAME #2> /dev/null
# echo "bw on $HOSTNAME"
# python3 ~/UGP/eagle/bandwidth/bandwidthd.py $command $HOSTNAME #2> /dev/null
echo "node info on $HOSTNAME"
python3 ~/UGP/eagle/nodeinfo/nodeinfo.py $command $HOSTNAME #2> /dev/null
