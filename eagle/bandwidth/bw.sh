#!/bin/bash
me=$1
binary=$2
hostfile=$3
bw=$4
tmpbw=$5

n=$(cat $hostfile | wc -l)
timeout 300 mpiexec -n $n -hostfile $hostfile $binary > $tmpbw

date > $bw.stamp
mv $tmpbw $bw
