import os, sys, time, subprocess, sqlite3, re, shutil
from pathlib import Path
try:
    home = str(Path.home())
except:
    home = os.getenv("HOME")
sys.path.insert(1, home+ '/UGP/eagle')
from daemon import Daemon


class EagleBandwidthDaemon(Daemon):
    def __init__(self, home, db , livehosts, script, binary,hostname,bw, pidfile, stdout='/dev/null', stderr='/dev/null', stdin='/dev/null'):
        super().__init__(pidfile, stdout, stderr , stdin )
        self.home = home
        self.db = db
        self.livehosts = livehosts
        self.script = script
        self.binary = binary
        self.hostname = hostname
        self.bw = bw

    def run(self):
        while True:
            open(self.stdout, 'w').close()
            # open(self.stderr, 'w').close()
            output = subprocess.run([self.script,self.hostname, self.binary, self.livehosts,self.bw ], stdout=subprocess.PIPE);
            bandwidths = output.stdout.decode("utf-8").strip(" \n" ).split('\n')
            db_input = [self.parse_bw(i) for i in bandwidths if i != ""]

            dump_string = ""
            for each in db_input:
                dump_string = dump_string + " ".join(str(i) for i in each) + "\n"
            with open(self.bw + ".tmp", 'w') as out:
                out.write(dump_string)
            shutil.move(self.bw + ".tmp", self.bw)

            # try:
            #     conn = sqlite3.connect(self.db)
            #     cur = conn.cursor()
            #     bw_sql = "INSERThome = str(Path.home())
            #     OR REPLACE INTO bw (hostA, hostB, bw) VALUES (?, ?, ?)"
            #     bw_monitor_sql = "INSERT OR REPLACE INTO bw_monitor (hostA, hostB, bw) VALUES (?, ?, ?)"
            #     cur.executemany(bw_sql, db_input)
            #     cur.executemany(bw_monitor_sql, db_input)
            #     conn.commit()
            #     conn.close()
            # except:
            #     time.sleep(0.2)
                
            time.sleep(180)

    def parse_bw(self,bw):
        bw = bw.split(" ")
        print(bw)
        bw[0] = int( re.findall('\d+', bw[0])[-1] )
        bw[1] = int( re.findall('\d+', bw[1])[-1] )
        bw[2] = int( bw[2])

        return [ bw[1] , bw[0], bw[2] ]



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

    pidfilename = home + "/.eagle/" + hostname + "/bwd.pid"
    stdout = home + "/.eagle/" + hostname + "/bwd.log"
    stderr = home + "/.eagle/" + hostname + "/bwd.err"
    bw = home + "/.eagle/" + hostname + "/bw.txt"
    db = home + "/.eagle/" + hostname + "/data.db"
    livehosts = home + "/.eagle/livehosts.txt"
    script= home + "/UGP/eagle/bandwidth/bandwidth.sh"
    binary = home + "/UGP/eagle/bandwidth/bandwidth.out"

    daemon = EagleBandwidthDaemon(home, db, livehosts, script, binary, hostname, bw, pidfilename, stdout, stderr)

    if 'start' == sys.argv[1]:
        print("bw Daemon on " + hostname + " : Starting")
        daemon.setupDB(db)
        daemon.start()
    elif 'stop' == sys.argv[1]:
        print("bw Daemon on " + hostname + " : Stoping")
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        print("bw Daemon on " + hostname + " : Restarting")
        daemon.setupDB(db)
        daemon.restart()
    else:
        print("Unknown command")
        sys.exit(2)

    sys.exit(0)

