import os, sys, time, subprocess, sqlite3, re, shutil, datetime
from pathlib import Path
try:
    home = str(Path.home())
except:
    home = os.getenv("HOME")
sys.path.insert(1, home+ '/UGP/eagle')

from daemon import Daemon

class EagleBandwidthDaemon(Daemon):
    def __init__(self, home, db , livehosts, script, binary,hostname,lt, tmplt, pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null'):
        super().__init__(pidfile, stdout, stderr , stdin )
        self.home = home
        self.db = db
        self.livehosts = livehosts
        self.script = script
        self.binary = binary
        self.hostname = hostname
        self.lt = lt
        self.tmplt = tmplt

    def run(self):
        while True:
            start = time.time()
            if os.stat(self.stdout).st_size > 256:
                open(self.stdout, 'w').close()
            if os.stat(self.stderr).st_size > 256:
                open(self.stderr, 'w').close()
            subprocess.run([self.script,self.hostname, self.binary, self.livehosts,self.lt, self.tmplt ], stdout=subprocess.PIPE)
            end = time.time()                
            print("Updated at {} , Took {}s".format( time.asctime( time.localtime( time.time() ) ), end - start) )
            time.sleep(15)


if __name__ == "__main__":
    output = subprocess.run(["hostname"], stdout=subprocess.PIPE)
    hostname = output.stdout.decode("utf-8").strip(" \n")

    if len(sys.argv) == 2:
        pass
    elif len(sys.argv) == 3:
        hostname = sys.argv[2]
    else:
        print("usage: " + sys.argv[0] + " start|stop|restart [hostname] ")
        sys.exit(2)

    hostname = hostname.split('.')[0].strip()

    if not os.path.isdir(home + "/.eagle/" + hostname):
        os.makedirs(home + "/.eagle/" + hostname, exist_ok=True)

    pidfilename = home + "/.eagle/" + hostname + "/ltd.pid"
    stdout = home + "/.eagle/" + hostname + "/ltd.log"
    stderr = home + "/.eagle/" + hostname + "/ltd.err"
    lt = home + "/.eagle/lt.txt"
    tmplt = home + "/.eagle/" + hostname + "/lt.txt"
    db = home + "/.eagle/" + hostname + "/data.db"
    livehosts = home + "/.eagle/livehosts.txt"
    script= home + "/UGP/eagle/latency/lt.sh"
    binary = home + "/UGP/eagle/latency/lt.out"

    daemon = EagleBandwidthDaemon(home, db, livehosts, script, binary, hostname, lt, tmplt, pidfilename, stdout, stderr)

    if 'start' == sys.argv[1]:
        print("lt Daemon on " + hostname + " : Starting")
        daemon.start()
    elif 'stop' == sys.argv[1]:
        print("lt Daemon on " + hostname + " : Stoping")
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        print("lt Daemon on " + hostname + " : Restarting")
        daemon.restart()
    else:
        print("Unknown command")
        sys.exit(2)

    sys.exit(0)

