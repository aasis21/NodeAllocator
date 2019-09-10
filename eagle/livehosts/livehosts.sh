#!/bin/bash
livehosts=$1
tmp=$2
printf "" > $tmp
# echo Checking live status of hosts ..
for id in {1..21}
do
    ssh -q -o ConnectTimeout=2 csews$id exit 
    status=$?
    echo $id $status
    if [ $status == '0' ]
    then
        echo csews$id >> $tmp
    fi
done

for id in {23..32}
do
    ssh -q -o ConnectTimeout=2 csews$id exit 
    status=$?
    echo $id $status
    if [ $status == '0' ]
    then
        echo csews$id >> $tmp
    fi
done

for id in {50..55}
do
    ssh -q -o ConnectTimeout=2 csews$id exit 
    status=$?
    echo $id $status
    if [ $status == '0' ]
    then
        echo csews$id >> $tmp
    fi
done
# for id in {80..90}
# do
#     ssh -q -o ConnectTimeout=2 csews$id exit 
#     status=$?
#     echo $id $status
#     if [ $status == '0' ]
#     then
#         echo csews$id >> $livehosts.tmp
#     fi
# done
mv $tmp $livehosts 