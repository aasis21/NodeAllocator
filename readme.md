# Network and Load-aware Resource Allocator for Parallel Programs
Distributed-memory parallel programs typically run on multiple nodes in a cluster (shared or dedicated) or a supercomputer. The parallel communication library (e.g. Message Passing Interface) takes care of the communication setup and messaging required for parallel execution. The user is expected to specify a list of nodes while executing a parallel job in an unmanaged cluster. Typically, users randomly select a few nodes without much knowledge about the current network connectivity of these nodes and the current load on these nodes. In this work, we address the problem of allocating a good set of nodes to run the parallel MPI jobs in a non-dedicated cluster with variable resource usages (varying compute load and varying available network bandwidths).

Parallel programs are generally communication-intensive. Thus the current available network bandwidth and latency between compute nodes impacts performance. Many existing resource allocation heuristics mainly consider static node attributes and a few dynamic resource attributes. This does not lead to a good allocation in case of shared clusters because the network usage and system load vary significantly at times. We present a load and network-aware greedy algorithm for resource allocation. We incorporated the current network state along with other static and dynamic resource characteristics in our heuristic. Our node allocator is lightweight, low-overhead and runs in a few milliseconds. We tested this on up to 60 heterogeneous nodes of our departmental cluster. It is able to reduce execution times of parallel benchmark codes by more than 40% on average as compared to the default.

This research work is done as a part of the Undergraduate Project, Fall Semester - 2019, under guidance of [Prof. Preeti Malakar](https://www.cse.iitk.ac.in/users/pmalakar/).

## Configuration and Usage Instruction
The Project consists of two component. One is eagle which monitor cluster live nodes, cluster current compute and network load. We use daemons that run on the cluster nodes in a distributed manner. The other one is allocator which uses the data provided by eagle to allocate specified number of nodes for user program.
### Eagle :
This consists of a number of daemon programs that keeps running on cluster in background.

 - **LivehostsD** : This runs on one of the cluster node. Periodically checks that for the live nodes in cluster and update the livehost list.
 - **NodeInfo**: Runs on each livehost and fetch node static and dynamic load data.
 - **bwD** : This runs on one of the livehosts. Internally runs a mpi program to calculate pair to pair bandwidth for all livehosts.
 - **ltD** : This also runs on one of the livehosts. Internally runs a mpi program to calculate pair to pair latency for all livehosts.
 - **monitorD**: This Daemon monitors the other Daemon and make sure they are running and if not so launch the required daemons.
##### Setting Up
Eagle uses `~/.eagle` to store all the monitoring information. Follows these steps to set up eagle.
 * Create eagle directory
``` bash
 > mkdir ~/.eagle
```
* 	create `hosts.txt` in `eagle` folder.
```
csews1
csews3
csews4
.
.
.
csews27
csews32
```
##### Starting up
* move to code repository and start monitord. Currently code repo should be in root folder and name should be UGP ( to be make configurable via environment variable).
```bash
> cd code_repo
> python3 eagle/monitor/monitord.py start
```

This will use `~/.eagle/hosts.txt` as nodes in cluster and launch all other daemon i.e `nodeinfod`, `bwd`, `ltd` on required nodes. This will keeps monitoring the daemon, if some daemon is not running, it will restart them.

##### Monitor
To manually check wheather the daeomon and running and if running then on which node. Run the following:
```bash
> cd code_repo
> ./eagle/monitor/globalDaemonStatus.sh  ~/.eagle/hosts.txt 
```
The output would be something like this:
```bash
>
csews1   :: nodeInfoD ::  up  
csews3   :: nodeInfoD ::  up  
.
.
.
csews32   :: nodeInfoD ::  up  
 
Monitord ::  :: csews19  
LiveHostsd ::  :: csews6  
ltd ::  :: csews6  
bwd ::  :: csews3  
```
##### Shut down
To shut the daemon off, stop the monitor daemon, it will kill all the other daemons.
```bash
> cd code_repo
> python3 eagle/monitor/monitord.py stop
```
##### `~/.eagle` directory structure
```
- hosts.txt
- livehosts.txt
- livehosts.txt.stamp
- bw.txt
- bw.txt.stamp
- lt.txt
- lt.txt.stamp
- csews1
	- nodeinfo.txt
	- nodeinfo.txt.stamp
	- nodeinfo.pid
- csews3 (also running bwd)
	- nodeinfo.txt
	- nodeinfo.txt.stamp
	- nodeinfo.pid
	- bwd.log
	- bwd.err
	- bwd.pid
....
....
....
- csews32
	- nodeinfo.txt
	- nodeinfo.txt.stamp
	- nodeinfo.pid
```
### Allocator :
This program uses the data provided by eagle to allocate specified number of nodes for user program. First create the binary and then use it for allocation.
```bash
> cd code_repo/allocator/src
> g++ allocator_improved.cpp -o allocator.out
```
use `allocator.out` for resourse allocation. This takes two arguments. One is process count and other is ppn.
```
> ./allocator.out 16 4

Output :
Allocated Nodes
csews3:4
csews11:4
csews7:4
csews9:4
```
This create two hostfile in code calling folder.
- hosts : Network and Load Aware hosts
- comphosts : Load Aware hosts

Use the host file to run mpi programs.
```bash
>  mpiexec -n 16 -hostfile hosts $mpi_program
>  n=32 &&  $allocator/allocator.out $n 4 > log &&  mpiexec -n $n -hostfile hosts $mpi_program
```


