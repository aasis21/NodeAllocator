#!/bin/bash
me=$1
binary=$2
hostfile=$3
lt=$4
tmplt=$5

n=$(cat $hostfile | wc -l)
timeout 120 mpiexec -n $n -hostfile $hostfile $binary > $tmplt
date > $lt.stamp
mv $tmplt $lt
