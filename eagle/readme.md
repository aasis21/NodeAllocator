## eagle : the eye of cluster
On each node of cluster we run an eagle daemon that monitors the system performance. Currently the information is kept in a json file. The daemon calculated bandwidth, cpu stats, etc  and update it in realtime. 
	
As we have nfs file system, each node have its performance json file which is updated by eagle in real time. File is in ~/.eagle/${hostname} folder.

### Running
- Start:  `python3 eagle.py start`
- Stop: `python3 eagle.py stop`
- Restart : `python3 eagle.py restart`

PS: Try running on local pc also.

