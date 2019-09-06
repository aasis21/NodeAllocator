import os, sys, time, subprocess, sqlite3, re, shutil
from pathlib import Path
try:
    home = str(Path.home())
except:
    home = os.getenv("HOME")
sys.path.insert(1, home+ '/UGP/eagle')
from daemon import Daemon


class EagleLatencyDaemon(Daemon):
    def __init__(self, home, db , livehosts, script, binary,hostname, latency, pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null'):
        super().__init__(pidfile, stdout, stderr , stdin )
        self.home = home
        self.db = db
        self.livehosts = livehosts
        self.script = script
        self.binary = binary
        self.hostname = hostname
        self.latency = latency
        self.old_latency = {}

    def run(self):
        while True:
            open(self.stdout, 'w').close()
            # open(self.stderr, 'w').close()
            output = subprocess.run([self.script, self.hostname, self.binary, self.livehosts, self.latency ], stdout=subprocess.PIPE)
            latencys = output.stdout.decode("utf-8").strip(" \n" ).split('\n')
            db_input = [self.parse_latency(i) for i in latencys if i != ""]

            for i in range(len(db_input)):
                if db_input[i][1] in self.old_latency:
                    old_latency = self.old_latency[db_input[i][1]]
                else:
                    old_latency = 0
                db_input[i][2] = 0.85 * old_latency + 0.15 * db_input[i][2]
                self.old_latency[db_input[i][1]] = db_input[i][2]

            dump_string = ""
            for each in db_input:
                dump_string = dump_string + " ".join(str(i) for i in each) + "\n"
            with open(self.latency + ".tmp", 'w') as out:
                out.write(dump_string)
            shutil.move(self.latency + ".tmp", self.latency)

            # try:
            #     conn = sqlite3.connect(self.db)
            #     cur = conn.cursor()
            #     latency_sql = "INSERT OR REPLACE INTO latency (hostA, hostB, latency) VALUES (?, ?, ?)"
            #     latency_monitor_sql = "INSERT OR REPLACE INTO latency_monitor (hostA, hostB, latency) VALUES (?, ?, ?)"
            #     cur.executemany(latency_sql, db_input)
            #     cur.executemany(latency_monitor_sql, db_input)
            #     conn.commit()
            #     conn.close()
            # except:
            #     time.sleep(0.2)


            time.sleep(30)

    def parse_latency(self,latency):
        latency = latency.split(" ")
        print(latency)
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

    pidfilename = home + "/.eagle/" + hostname + "/latencyd.pid"
    stdout = home + "/.eagle/" + hostname + "/latencyd.log"
    stderr = home + "/.eagle/" + hostname + "/latencyd.err"
    latency = home + "/.eagle/" + hostname + "/latency.txt"
    db = home + "/.eagle/" + hostname + "/data.db"
    livehosts = home + "/.eagle/livehosts.txt"
    script= home + "/UGP/eagle/latency/latency.sh"
    binary = home + "/UGP/eagle/latency/latency.out"

    daemon = EagleLatencyDaemon(home, db, livehosts, script, binary, hostname,latency, pidfilename, stdout, stderr)
    
    if 'start' == sys.argv[1]:
        print("latency Daemon on " + hostname + " : Starting")
        daemon.setupDB(db)
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