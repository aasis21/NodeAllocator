#!/bin/bash
for i in 64 80 96
do
	echo "process= $i"
	./run_tests.sh $i | tee log$i.txt
done

