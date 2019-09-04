#!/bin/bash
eagle="$HOME/.eagle/$HOSTNAME/nodeinfo.pid"
latency="$HOME/.eagle/$HOSTNAME/latencyd.pid"
bw="$HOME/.eagle/$HOSTNAME/bwd.pid"
livehosts="$HOME/.eagle/$HOSTNAME/livehosts.pid"

printf "$HOSTNAME  ::: "
if [ -f $eagle ]; then
   printf "nodeInfod : up "
else
   printf "nodeInfod : down "
fi

printf " :: "

if [ -f $latency ]; then
   printf "latencyd : up "
else
   printf "latencyd : down "
fi

printf " :: "

if [ -f $bw ]; then
   printf "bwd : up "
else
   printf "bwd : down "
fi

printf " :: "

if [ -f $livehosts ]; then
   printf "livehosts : up "
else
   printf "livehosts : down "
fi
echo " "
