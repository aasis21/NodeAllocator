#!/bin/bash
HOSTNAME=csews4
eagle="$HOME/.eagle/$HOSTNAME/nodeinfo.pid"
latency="$HOME/.eagle/$HOSTNAME/ltd.pid"
bw="$HOME/.eagle/$HOSTNAME/bwd.pid"
livehosts="$HOME/.eagle/$HOSTNAME/livehosts.pid"
monitor="$HOME/.eagle/$HOSTNAME/monitor.pid"


printf "$HOSTNAME  ::: "
if [ -f $eagle ]; then
   pid=`cat $eagle`
   ps -p $pid &>/dev/null
   if [ $? -eq 0 ]; then
      printf "nodeinfod : up "
   else
      printf "nodeinfod : down "
   fi
else
   printf "nodeInfod : down "
fi

printf " :: "

if [ -f $latency ]; then
   pid=`cat $latency`
   ps --pid $pid &>/dev/null
   if [ $? -eq 0 ]; then
      printf "latencyd : up "
   else
      printf "latencyd : down "
   fi

else
   printf "latencyd : down "
fi

printf " :: "

if [ -f $bw ]; then
   pid=`cat $bw`
   ps -p $pid &>/dev/null
   if [ $? -eq 0 ]; then
      printf "bwd : up "
   else
      printf "bwd : down "
   fi
else
   printf "bwd : down "
fi

printf " :: "

if [ -f $livehosts ]; then
   pid=`cat $livehosts`
   ps --pid $pid &>/dev/null
   if [ $? -eq 0 ]; then
      printf "livehosts : up "
   else
      printf "livehosts : down "
   fi
else
   printf "livehosts : down "
fi


printf " :: "

if [ -f $monitor ]; then
   pid=`cat $monitor`
   ps --pid $pid &>/dev/null
   if [ $? -eq 0 ]; then
      printf "monitor : up "
   else
      printf "monitor : down "
   fi
else
   printf "monitor : down "
fi

echo " "
