#!/bin/bash
for p in  4 8 16 32 64
do
echo "running :: Process count = $p"

    for s in 8 16 24 32 40 48
    do
        echo "================================================================================================================================================================================"
        echo "running :: process count = $p problem size = $s"
        for j in 1 2 3 4 5
        do
            echo "-------------------------------------------------    running :: process count = $p problem size = $s iteration = $j   --------------------------------------------------"
            ~/UGP/allocator/run.sh $p 4 ~/UGP/allocator/miniMD -s $s -n 500
            echo "----------------------------------------------------------- ------------------------------------------------------------------------------------------------------------"
        done
        echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    done

done
# cat result.log | grep "Total Time :" | awk '{print $NF}' > time.txt
# python3 data.py < time.txt