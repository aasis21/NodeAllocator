import os
import sys
import time
import psutil
import json
from pathlib import Path
from daemon import Daemon
from collections import deque

class NetworkNode:
    def __init__(self, rx,tx,time):
        self.rx = rx
        self.tx = tx
        self.time = time

class EagleDaemon(Daemon):
    def __init__(self, statfile , pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null'):
        super().__init__(pidfile, stdout, stderr , stdin )
        self.networkDeque =  deque(maxlen = 150)
        self.statfile = statfile

    def run(self):
        while True:
            stats = {}
            stats["bandwidth"] = self.bandwidth()
            stats["cpuStat"] = self.getCpuStats()
            with open(self.statfile,'w+',encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=4)
            time.sleep(2)

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
            

    def getCpuStats(self):
        cpuStats = {}
        cpuTimes = psutil.cpu_times()
        cpuStats["cpuTimes"] = { 
            "user" : cpuTimes.user,
            "sys" : cpuTimes.system,
            "idle" : cpuTimes.idle,
            "iowait" : cpuTimes.iowait
        }
        
        cpuStats["cpuCount"] = psutil.cpu_count()
        cpuStats["coreCount"] = psutil.cpu_count(logical=False)
        
        cpufreq = psutil.cpu_freq()
        cpuStats["cpufreq"] = {"cur" : cpufreq.current, "min" : cpufreq.min, "max" :cpufreq.max , "avg" : 0 }
        cpuStats["cpuload"] = psutil.getloadavg()

        return cpuStats


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
    daemon = EagleDaemon(statfile, pidfilename, stdout, stderr)

    if 'start' == sys.argv[1]:
        print("bw Daemon on " + hostname + " : Starting")
        daemon.start()
    elif 'stop' == sys.argv[1]:
        print("bw Daemon on " + hostname + " : Stop")
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        print("bw Daemon on " + hostname + " : Restart")
        daemon.restart()
    else:
        print("Unknown command")
        sys.exit(2)
        sys.exit(0)

