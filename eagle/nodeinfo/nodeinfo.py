import os, sys, time, subprocess, psutil, json, sqlite3, re, shutil
from pathlib import Path
try:
    home = str(Path.home())
except:
    home = os.getenv("HOME")

sys.path.insert(1, home+ '/UGP/eagle')
from daemon import Daemon
from collections import deque

class NetworkNode:
    def __init__(self, rx,tx,time):
        self.rx = rx
        self.tx = tx
        self.time = time

class UtilizationNode:
    def __init__(self, user, system, idle, iowait, time):
        self.user = user
        self.system = system
        self.idle = idle
        self.iowait =iowait
        self.time = time

class EagleNodeDaemon(Daemon):
    def __init__(self, hostname, home, script, statfile , pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null'):
        super().__init__(pidfile, stdout, stderr , stdin )
        self.hostname = hostname
        self.home = home
        self.script = script
        self.statfile = statfile
        self.networkDeque =  deque(maxlen = 150)
        self.utilizationDeque =  [ deque(maxlen = 10), deque(maxlen = 50), deque(maxlen = 150)]
        self.utilizationSum = [0.0,0.0,0.0]
        self.memorySum = [0.0, 0.0, 0.0]
        self.memoryDeque =  [ deque(maxlen = 10), deque(maxlen = 50), deque(maxlen = 150)]

    def run(self):
        while True:
            print("Start")
            start = time.time()
            
            if os.stat(self.stdout).st_size > 256:
                open(self.stdout, 'w').close()
            if os.stat(self.stderr).st_size > 256:
                open(self.stderr, 'w').close()


            cpuCount = psutil.cpu_count(logical=True)
            coreCount = psutil.cpu_count(logical=False)
            cpu_freq = psutil.cpu_freq()
            cpuFreq = [int(cpu_freq.min),int(cpu_freq.current), int(cpu_freq.max)]

            nodeLoad = psutil.getloadavg()
            nodeUtilization = self.utilization()
            nodeBandwidth = self.bandwidth()
            nodeMemory = self.memory()
            users = len(psutil.users())

            stats = {
                'cpucount': cpuCount,
                'corecount':coreCount,
                'cpufreq': cpuFreq,
                'nodeload': nodeLoad,
                'nodeutilization': nodeUtilization,
                'nodebandwidth' : nodeBandwidth,
                'nodeMemory': nodeMemory,
                'nodeusers' : users
            }

            db_input = [hostname,cpuCount, coreCount] + cpuFreq + list(nodeLoad) + nodeBandwidth + nodeUtilization + nodeMemory + [users]

            db_string = ' '.join([str(elem) for elem in db_input]) 
            with open(self.statfile + ".tmp", 'w') as out:
                out.write(db_string)
            shutil.move(self.statfile + ".tmp", self.statfile)
            subprocess.run([self.script, self.statfile], stdout=subprocess.PIPE)

            end = time.time()                
            print("Updated at {} , Took {}s".format( time.asctime( time.localtime( time.time() ) ), end - start) )
            time.sleep(5)            

    def bandwidth(self):
        # push to deque
        net_io = psutil.net_io_counters()
        n_node = NetworkNode(net_io.bytes_recv, net_io.bytes_sent, time.time())
        self.networkDeque.appendleft(n_node)
        n_deque = self.networkDeque

        # do calculation
        l = len(n_deque)
        if l < 30:
            n_band =  [0.0,0.0,0.0]
        elif l < 150:
            n_band = [ ( n_deque[0].rx - n_deque[4].rx ) / ( n_deque[0].time - n_deque[4].time ) , 
                        ( n_deque[0].rx - n_deque[l//3].rx ) / ( n_deque[0].time - n_deque[l//3].time ) ,
                        ( n_deque[0].rx - n_deque[l-1].rx ) / ( n_deque[0].time - n_deque[l-1].time ) 
            ]    
        else:
            n_band = [ ( n_deque[0].rx - n_deque[4].rx ) / ( n_deque[0].time - n_deque[4].time ) , 
                        ( n_deque[0].rx - n_deque[l//5].rx ) / ( n_deque[0].time - n_deque[l//5].time ) ,
                        ( n_deque[0].rx - n_deque[l-1].rx ) / ( n_deque[0].time - n_deque[l-1].time ) 
            ]
        
        return [int(n_band[0]//1000000), int(n_band[1]//1000000), int(n_band[2]//1000000) ]
            
    def utilization(self):
        utilization = psutil.cpu_percent()

        def manageQueue(node, index):
            queue = self.utilizationDeque[index]
            if len(queue) == 0:
                queue.appendleft(node)
                self.utilizationSum[index] = node
            else:
                if len(queue) == queue.maxlen:
                    removeNode = queue.pop()
                else:
                    removeNode = 0  
                self.utilizationSum[index] = node + self.utilizationSum[index] - removeNode
                queue.appendleft(node)

            return int(self.utilizationSum[index] // len(queue))
        return [ manageQueue(utilization, i) for i in range(3) ]

    def memory(self):
        memory = psutil.virtual_memory()
        total = memory.total

        def manageQueue(node, index):
            queue = self.memoryDeque[index]
            if len(queue) == 0:
                queue.appendleft(node)
                self.memorySum[index] = node
            else:
                if len(queue) == queue.maxlen:
                    removeNode = queue.pop()
                else:
                    removeNode = 0  

                self.memorySum[index] = node + self.memorySum[index] - removeNode
                queue.appendleft(node)

            return self.memorySum[index] // ( len(queue) * 1000000 )

        return [total] + [ manageQueue(memory.available, i) for i in range(3) ]


if __name__ == "__main__":
    output = subprocess.run(["hostname"], stdout=subprocess.PIPE)
    hostname = output.stdout.decode("utf-8").strip(" \n")

    if len(sys.argv) == 2:
        pass
    elif len(sys.argv) == 3:
        hostname = sys.argv[2]
        hostname = hostname.split('.')[0].strip()
    else:
        print("usage: " + sys.argv[0] + " start|stop|restart [hostname] ")
        sys.exit(2)

    hostname = hostname.split('.')[0].strip()

    if not os.path.isdir(home + "/.eagle/" + hostname):
        os.makedirs(home + "/.eagle/" + hostname, exist_ok=True)

    pidfilename = home + "/.eagle/" + hostname + "/nodeinfo.pid"
    stdout = home + "/.eagle/" + hostname + "/nodeinfo.log"
    stderr = home + "/.eagle/" + hostname + "/nodeinfo.err"
    statfile = home + "/.eagle/" + hostname + "/nodeinfo.txt"
    script= home + "/UGP/eagle/nodeinfo/stamp.sh"
    daemon = EagleNodeDaemon(hostname, home, script, statfile, pidfilename, stdout, stderr)

    if 'start' == sys.argv[1]:
        print("Node Daemon on " + hostname + " : Starting")
        daemon.start()
    elif 'stop' == sys.argv[1]:
        print("Node Daemon on " + hostname + " : Stop")
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        print("Node Daemon on " + hostname + " : Restart")
        daemon.restart()
    else:
        print("Unknown command")
        sys.exit(2)
    
    sys.exit(0)

