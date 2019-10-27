import os, sys, time, subprocess, sqlite3, re
from pathlib import Path
try:
    home = str(Path.home())
except:
    home = os.getenv("HOME")
sys.path.insert(1, home+ '/UGP/eagle')
from daemon import Daemon


class EagleLiveHostsDaemon(Daemon):
    def __init__(self, home, hosts , livehosts, tmplivehosts, script, hostname, pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null'):
        super().__init__(pidfile, stdout, stderr , stdin )
        self.home = home
        self.hosts = hosts
        self.livehosts = livehosts
        self.script = script
        self.hostname = hostname
        self.tmplivehosts = tmplivehosts

    def run(self):
        while True:
            start = time.time()
            if os.stat(self.stdout).st_size > 256:
                open(self.stdout, 'w').close()
            if os.stat(self.stderr).st_size > 256:
                open(self.stderr, 'w').close()
            
            subprocess.run([self.script, self.hosts, self.livehosts, self.tmplivehosts], stdout=subprocess.PIPE)

            end = time.time()                
            print("Updated at {} , Took {}s".format( time.asctime( time.localtime( time.time() ) ), end - start) )
            time.sleep(180)

if __name__ == "__main__":

    output = subprocess.run(["hostname"], stdout=subprocess.PIPE)
    hostname = output.stdout.decode("utf-8").strip(" \n")
    
    if len(sys.argv) == 2:
        pass
    elif len(sys.argv) == 3:
        hostname = sys.argv[2]
        hostname = hostname.split('.')[0].strip()
    else:
        print("usages: " + sys.argv[0] + " start|stop|restart [hostname] ")
        sys.exit(2)
    
    hostname = hostname.split('.')[0].strip()

    if not os.path.isdir(home + "/.eagle/" + hostname):
        os.makedirs(home + "/.eagle/" + hostname, exist_ok=True)

    pidfilename = home + "/.eagle/" + hostname + "/livehosts.pid"
    stdout = home + "/.eagle/" + hostname + "/livehosts.log"
    stderr = home + "/.eagle/" + hostname + "/livehosts.err"
    
    hosts= home + "/.eagle/hosts.txt"
    livehosts = home + "/.eagle/livehosts.txt"
    tmplivehosts = home + "/.eagle/" + hostname + "/livehosts.txt"
    script= home + "/UGP/eagle/livehosts/livehosts.sh"

    daemon = EagleLiveHostsDaemon(home, hosts, livehosts,tmplivehosts, script, hostname, pidfilename, stdout, stderr)

    if 'start' == sys.argv[1]:
        print("latency Daemon on " + hostname + " : Starting")
        daemon.start()
    elif 'stop' == sys.argv[1]:
        print("latency Daemon on " + hostname + " : Stop")
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        print("latency Daemon on " + hostname + " : Restart")
        daemon.setupDB(db)
        daemon.restart()
    else:
        print("Unknown command")
        sys.exit(2)
    
    sys.exit(0)
