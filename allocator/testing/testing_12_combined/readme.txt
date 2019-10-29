## Runnning test
The result.log contains the allocated nodes and time data for each process and problem size
The metadata.log contains metadata and cluster state at time of allocations, both file are generated
via testing script run_test.sh.

## Parse data and plot graph
cat result.log | grep "Total Time :" | awk '{print $NF}' > time.txt
python3 data.py < time.txt