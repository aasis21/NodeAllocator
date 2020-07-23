#!/bin/bash
me=$1
binary=$2
hostfile=$3
bw=$4
tmpbw=$5

n=$(cat $hostfile | wc -l)
timeout 300 mpiexec -n $n -hostfile $hostfile $binary > $tmpbw

date > $bw.stamp
date >> $bw.alltime
head -5 $tmpbw | tail -1 && date >> $bw.track1
head -50 $tmpbw | tail -1 && date >> $bw.track2
head -100 $tmpbw | tail -1 && date >> $bw.track3
head -150 $tmpbw | tail -1 && date >> $bw.track4
head -170 $tmpbw | tail -1 && date >> $bw.track5
head -190 $tmpbw | tail -1 && date >> $bw.track6
head -350 $tmpbw | tail -1 && date >> $bw.track7
head -500 $tmpbw | tail -1 && date >> $bw.track8
head -600 $tmpbw | tail -1 && date >> $bw.track9

mv $tmpbw $bw
