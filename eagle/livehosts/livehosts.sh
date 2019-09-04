#!/bin/bash
livehosts=$1
printf "" > $livehosts.tmp
# echo Checking live status of hosts ..
for id in {1..50}
do
    ssh -q -o ConnectTimeout=2 csews$id exit 
    status=$?
    echo $id $status
    if [ $status == '0' ]
    then
        echo csews$id >> $livehosts.tmp
    fi
done
mv $livehosts.tmp $livehosts 