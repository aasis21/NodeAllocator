import os, sys, time, subprocess, sqlite3, re, random
from pathlib import Path
try:
    home = str(Path.home())
except:
    home = os.getenv("HOME")
sys.path.insert(1, home+ '/UGP/eagle')

from daemon import Daemon


class EagleMonitorDaemon(Daemon):
    def __init__(self, home , hosts, script, pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null'):
        super().__init__(pidfile, stdout, stderr , stdin )
        self.home = home
        self.script = script
        self.hosts = hosts

    def run(self):
        while True:
            start = time.time()
            if os.stat(self.stdout).st_size > 1024:
                open(self.stdout, 'w').close()
            if os.stat(self.stderr).st_size > 1024:
                open(self.stderr, 'w').close()
            
            output = subprocess.run([self.script , self.hosts ], stdout=subprocess.PIPE)
            status = output.stdout.decode("utf-8").strip(" \n" ).split('\n')
            status = [self.parse_status(i) for i in status if i != ""]

            hosts=[]
            bwd_s=[]
            ltd_s=[]
            livehostd_s=[]
            for st in status:
                hosts.append(st[0])
                if(st[1]=='down'):
                    host = st[0]
                    subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/nodeinfo/nodeinfo.py start {}".format(self.home,host) ], stdout=subprocess.PIPE)
               
                if(st[2]=='up'):
                    ltd_s.append(st[0])                
                if(st[3]=='up'):
                    bwd_s.append(st[0])
                if(st[4]=='up'):
                    livehostd_s.append(st[0])

            if(len(ltd_s) == 0):
                host = random.choice(hosts)
                subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/latency/latencyd.py start {}".format(self.home, host) ], stdout=subprocess.PIPE)
                ltd_s.append(host)
            elif(len(ltd_s)>1):
                for host in bwd_s[1:]:
                    print(host)
                    subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/latency/latencyd.py stop {}".format(self.home, host) ], stdout=subprocess.PIPE)

            if(len(bwd_s) == 0):
                host = random.choice(hosts)
                subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/bandwidth/bandwidthd.py start {}".format(self.home, host) ], stdout=subprocess.PIPE)
                bwd_s.append(host)
            elif(len(bwd_s)>1):
                for host in bwd_s[1:]:
                    print(host)
                    subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/bandwidth/bandwidthd.py stop {}".format(self.home, host) ], stdout=subprocess.PIPE)

            if(len(livehostd_s) == 0):
                host = random.choice(hosts)
                subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/livehosts/livehostsd.py start {}".format(self.home, host) ], stdout=subprocess.PIPE)
                livehostd_s.append(host)
            elif(len(livehostd_s)>1):
                for host in livehostd_s[1:]:
                    print(host)
                    subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/livehosts/livehostsd.py stop {}".format(self.home, host) ], stdout=subprocess.PIPE)

            end = time.time()                
            print("Updated at {} , Took {}s".format( time.asctime( time.localtime( time.time() ) ), end - start) )
            print("ltd : ", ltd_s[0], " bwd : ", bwd_s[0], " livehostsd : ", livehostd_s[0] )
            time.sleep(30)

    def prepare_stop(self):
        start = time.time()
        output = subprocess.run([self.script , self.hosts ], stdout=subprocess.PIPE)
        status = output.stdout.decode("utf-8").strip(" \n" ).split('\n')
        status = [self.parse_status(i) for i in status if i != ""]
        for st in status:
            host = st[0]
            subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/nodeinfo/nodeinfo.py stop {}".format(self.home,host) ], stdout=subprocess.PIPE)
            subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/latency/latencyd.py stop {}".format(self.home, host) ], stdout=subprocess.PIPE)
            subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/bandwidth/bandwidthd.py stop {}".format(self.home, host) ], stdout=subprocess.PIPE)
            subprocess.run(["ssh" , "-q" , "-o" , "ConnectTimeout=2", host, "python3 {}/UGP/eagle/livehosts/livehostsd.py stop {}".format(self.home, host) ], stdout=subprocess.PIPE)
        end = time.time()                
        print("Stopped at {} , Took {}s".format( time.asctime( time.localtime( time.time() ) ), end - start) )


    def parse_status(self,status):
        status = ' '.join( status.replace(":", "").split()).split()
        st = [ status[0],  status[2], status[4], status[6], status[8]]
        return st

if __name__ == "__main__":

    output = subprocess.run(["hostname"], stdout=subprocess.PIPE)
    hostname = output.stdout.decode("utf-8").strip(" \n")
    hostname = hostname.split('.')[0].strip()

    if not os.path.isdir(home + "/.eagle/" + hostname):
        os.makedirs(home + "/.eagle/" + hostname, exist_ok=True)

    pidfilename = home + "/.eagle/" + hostname + "/monitor.pid"
    stdout = home + "/.eagle/" + hostname + "/monitor.log"
    stderr = home + "/.eagle/" + hostname + "/monitor.err"
    script= home + "/UGP/eagle/monitor/monitor_script.sh"
    hosts= home + "/.eagle/hosts.txt"

    daemon = EagleMonitorDaemon(home, hosts, script, pidfilename, stdout, stderr)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print("livehosts Daemon on " + hostname + " : Starting")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print("livehosts Daemon on " + hostname + " : Stoping")
            daemon.prepare_stop()
            daemon.stop()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: " + sys.argv[0] + "  start|stop|restart")
        sys.exit(2)
