#!/bin/bash
me=$1
binary=$2
hostfile=$3
bw=$4
tmpbw=$5

n=$(cat $hostfile | wc -l)
timeout 450 mpiexec -n $n -hostfile $hostfile $binary > $tmpbw

date > $bw.stamp
date >> $bw.alltime

( echo  `date` && grep "csews32 csews3 " $tmpbw ) >> $bw.t1
( echo  `date` && grep "csews3 csews32 " $tmpbw ) >> $bw.t1
( echo  `date` && grep "csews1 csews10 " $tmpbw ) >> $bw.t2
( echo  `date` && grep "csews10 csews1 " $tmpbw ) >> $bw.t2
( echo  `date` && grep "csews14 csews26 " $tmpbw ) >> $bw.t3
( echo  `date` && grep "csew26 csews14 " $tmpbw ) >> $bw.t3
( echo  `date`  && grep "csews26 csews16 " $tmpbw ) >> $bw.t4
( echo  `date`  && grep "csews16 csews26 " $tmpbw ) >> $bw.t4




mv $tmpbw $bw
