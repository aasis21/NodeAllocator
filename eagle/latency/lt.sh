#!/bin/bash
me=$1
binary=$2
hostfile=$3
lt=$4
tmplt=$5

n=$(cat $hostfile | wc -l)
timeout 120 mpiexec -n $n -hostfile $hostfile $binary > $tmplt
date > $lt.stamp
date >> $lt.alltime

( echo -n `date` && printf " " && grep "csews32 csews3 " $tmplt ) >> $lt.t1
( echo -n `date` && printf " " && grep "csews3 csews32 " $tmplt ) >> $lt.t1
( echo -n `date` && printf " " && grep "csews1 csews10 " $tmplt ) >> $lt.t2
( echo -n `date` && printf " " && grep "csews10 csews1 " $tmplt ) >> $lt.t2
( echo -n `date` && printf " " && grep "csews14 csews26 " $tmplt ) >> $lt.t3
( echo -n `date` && printf " " && grep "csew26 csews14 " $tmplt ) >> $lt.t3
( echo -n `date` && printf " " && grep "csews26 csews16 " $tmplt ) >> $lt.t4
( echo -n `date` && printf " " && grep "csews16 csews26 " $tmplt ) >> $lt.t4


mv $tmplt $lt
