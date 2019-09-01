import os, sys, time, subprocess, psutil, json, sqlite3, re
from pathlib import Path
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
    def __init__(self, home, db, statfile , pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null'):
        super().__init__(pidfile, stdout, stderr , stdin )
        self.home = home
        self.db = db
        self.statfile = statfile
        self.networkDeque =  deque(maxlen = 150)
        self.utilizationDeque =  [ deque(maxlen = 10), deque(maxlen = 50), deque(maxlen = 150)]
        self.utilizationSum = [0.0,0.0,0.0]
        self.memorySum = [0.0, 0.0, 0.0]
        self.memoryDeque =  [ deque(maxlen = 10), deque(maxlen = 50), deque(maxlen = 150)]

    def run(self):
        while True:
            print("time0: " + str( time.time() ) ) 
            cpuCount = psutil.cpu_count(logical=True)
            coreCount = psutil.cpu_count(logical=False)
            cpu_freq = psutil.cpu_freq()
            cpuFreq = [cpu_freq.min,cpu_freq.current, cpu_freq.max]

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
            
            print("time1: " + str( time.time() ) ) 
            with open(self.statfile,'w+',encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=4)
            print("time2: " + str( time.time() ) ) 
            # time.sleep(1)


    def bandwidth(self):
        # push to deque
        net_io = psutil.net_io_counters()
        n_node = NetworkNode(net_io.bytes_recv, net_io.bytes_sent, time.time())
        self.networkDeque.appendleft(n_node)
        n_deque = self.networkDeque

        # do calculation
        l = len(n_deque)
        if l < 30:
            n_band =  [0,0,0]
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
        
        return n_band
            
    def utilizationByCategory(self):
        utilization = psutil.cpu_times_percent()
        node = UtilizationNode(utilization.user, utilization.system, utilization.idle, utilization.iowait, time.time() )

        def manageQueue(node,queue):
            if len(queue) == 0:
                queue.appendleft(node)
            else:
                topNode = queue[0]
                if len(queue) == queue.maxlen:
                    removeNode = queue.pop()
                else:
                    removeNode = UtilizationNode(0,0,0,0,time.time())
                    
                newNode = UtilizationNode(
                    node.user + topNode.user - removeNode.user,
                    node.system + topNode.system - removeNode.system,
                    node.idle + topNode.idle - removeNode.idle,
                    node.iowait + topNode.iowait - removeNode.iowait,
                    time.time()
                )
                queue.appendleft(newNode)
            
            topNode = queue[0]
            l = len(queue)
            return [topNode.user/l,topNode.system/l,topNode.idle/l,topNode.iowait/l]

        return [ manageQueue(node, self.utilizationDeque[i]) for i in range(3) ]

    def utilization(self):
        utilization = psutil.cpu_percent()

        def manageQueue(node, index):
            queue = self.utilizationDeque[index]
            if len(queue) == 0:
                queue.appendleft(node)
                newNodesSum = node
            else:
                if len(queue) == queue.maxlen:
                    removeNode = queue.pop()
                else:
                    removeNode = 0  
                newNodesSum = node + nodes_sum - removeNode

                queue.appendleft(node)
            
            self.utilizationSum[index] = newNodesSum
            return newNodesSum / len(queue)

        return [ manageQueue(utilization, i) for i in range(3) ]

    def memory(self):
        memory = psutil.virtual_memory()
        total = memory.total

        def manageQueue(node, index):
            queue = self.memoryDeque[index]
            if len(queue) == 0:
                queue.appendleft(node)
                newNodesSum = node
            else:
                if len(queue) == queue.maxlen:
                    removeNode = queue.pop()
                else:
                    removeNode = 0  
                newNodesSum = node + nodes_sum - removeNode

                queue.appendleft(node)
            
            self.memorySum[index] = newNodesSum
            return newNodesSum / len(queue)

        return [total] + [ manageQueue(memory.available , self.memoryDeque[i]) for i in range(3) ]


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

    home = str(Path.home())
    if not os.path.isdir(home + "/.eagle/" + hostname):
        os.makedirs(home + "/.eagle/" + hostname, exist_ok=True)

    pidfilename = home + "/.eagle/" + hostname + "/eagle.pid"
    stdout = home + "/.eagle/" + hostname + "/eagle.log"
    stderr = home + "/.eagle/" + hostname + "/eagle.err"
    statfile = home + "/.eagle/" + hostname + "/eagle.json"
    db = home + "/.eagle/" + hostname + "/data.db"
    daemon = EagleNodeDaemon(home, db, statfile, pidfilename, stdout, stderr)

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

