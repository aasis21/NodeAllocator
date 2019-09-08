import os, sys, time, subprocess, sqlite3, re, shutil
from pathlib import Path
try:
    home = str(Path.home())
except:
    home = os.getenv("HOME")
sys.path.insert(1, home+ '/UGP/eagle')
from daemon import Daemon


class EagleTopologyDaemon(Daemon):
    def __init__(self, home, db , script, binary, tphosts, hostname, pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null'):
        super().__init__(pidfile, stdout, stderr , stdin )
        self.home = home
        self.db = db
        self.script = script
        self.binary = binary
        self.hostname = hostname
        self.tphosts = tphosts

    def run(self):
        while True:
            # open(self.stdout, 'w').close()
            # open(self.stderr, 'w').close()
            output = subprocess.run([self.script, self.hostname, self.binary, self.tphosts], stdout=subprocess.PIPE)
            # latencys = output.stdout.decode("utf-8").strip(" \n" ).split('\n')
            # db_input = [self.parse_latency(i) for i in latencys if i != ""]

            # print(db_input)
            # try:
            #     conn = sqlite3.connect(self.db)
            #     cur = conn.cursor()
            #     latency_sql = "INSERT OR REPLACE INTO latency (hostA, hostB, latency) VALUES (?, ?, ?)"
            #     latency_monitor_sql = "INSERT OR REPLACE INTO latency_monitor (hostA, hostB, latency) VALUES (?, ?, ?)"
            #     cur.executemany(latency_monitor_sql, db_input)
            #     conn.commit()
            #     conn.close()
            # except:
            #     time.sleep(0.2)


            time.sleep(30)

    def parse_latency(self,latency):
        latency = latency.split(" ")
        latency[0] = int( re.findall('\d+', latency[0])[-1] )
        latency[1] = int( re.findall('\d+', latency[1])[-1] )
        latency[2] = int( latency[2])
        return [ latency[0] , latency[1], latency[2] ]


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

    if not os.path.isdir(home + "/.eagle/" + hostname):
        os.makedirs(home + "/.eagle/" + hostname, exist_ok=True)

    pidfilename = home + "/.eagle/" + hostname + "/tpd.pid"
    stdout = home + "/.eagle/" + hostname + "/tpd.log"
    stderr = home + "/.eagle/" + hostname + "/tpd.err"
    db = home + "/.eagle/" + hostname + "/tpdata.db"
    script= home + "/UGP/eagle/topology/tp.sh"
    binary = home + "/UGP/eagle/latency/latency.out"
    tphosts = home + "/.eagle/" + hostname + "/tphosts.txt"

    daemon = EagleTopologyDaemon(home, db, script, binary, tphosts, hostname, pidfilename, stdout, stderr)
    
    if 'start' == sys.argv[1]:
        print("TP Daemon on " + hostname + " : Starting")
        daemon.setupDB(db)
        daemon.start()
    elif 'stop' == sys.argv[1]:
        print("TP Daemon on " + hostname + " : Stop")
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        print("TP Daemon on " + hostname + " : Restart")
        daemon.setupDB(db)
        daemon.restart()
    else:
        print("Unknown command")
        sys.exit(2)
    
    sys.exit(0)