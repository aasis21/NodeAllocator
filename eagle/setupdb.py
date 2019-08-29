import os, sys, time, sqlite3
from pathlib import Path


if __name__ == "__main__":
    try:
        hostname = os.environ["HOSTNAME"]
    except:
        hostname = "localhost"
        
    if hostname == "":
        hostname = "localhost"
    else:
        hostname = hostname.split('.')[0].strip()

    if len(sys.argv) == 2:
        hostname = sys.argv[2]
        hostname = hostname.split('.')[0].strip()

    home = str(Path.home())
    if not os.path.isdir(home + "/.eagle/"):
        os.makedirs(home + "/.eagle/", exist_ok=True)

    db = home + "/.eagle/data.db"
    con = sqlite3.connect(db)
    cur = con.cursor()
    
    latency_sql = """
    CREATE TABLE latency (
        hostA INTEGER NOT NULL,
        hostB INTEGER NOT NULL,
        latency INTEGER NOT NULL,
        time TIMESTAMP DEFAULT  (strftime('%s','now')),
        PRIMARY KEY (hostA, hostB)
    )"""

    try:
        cur.execute(latency_sql)
    except:
        print("Latency table exists.. ")

    latency_monitor_sql = """
    CREATE TABLE latency_monitor (
        id INTEGER PRIMARY KEY,
        hostA INTEGER NOT NULL,
        hostB INTEGER NOT NULL,
        latency INTEGER NOT NULL,
        time TIMESTAMP DEFAULT  (strftime('%s','now'))
    )"""
    try:
        cur.execute(latency_monitor_sql)
    except:
        print("Latency monitor table exists.. ")

    bw_sql = """
    CREATE TABLE bw (
        hostA INTEGER NOT NULL,
        hostB INTEGER NOT NULL,
        bw INTEGER NOT NULL,
        time TIMESTAMP DEFAULT  (strftime('%s','now')),
        PRIMARY KEY (hostA, hostB)
    )"""

    try:
        cur.execute(bw_sql)
    except:
        print("BW table exists.. ")

    bw_monitor_sql = """
    CREATE TABLE bw_monitor (
        id INTEGER PRIMARY KEY,
        hostA INTEGER NOT NULL,
        hostB INTEGER NOT NULL,
        bw INTEGER NOT NULL,
        time TIMESTAMP DEFAULT  (strftime('%s','now'))
    )"""
    try:
        cur.execute(bw_monitor_sql)
    except:
        print("BW monitor table exists.. ")
    
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(cur.fetchall())

    # print("seeing data")
    # for row in cur.execute('SELECT * FROM latency ORDER BY hostA'):
    #     print(row)

    # print("*****************************************************************")

    # for row in cur.execute('SELECT * FROM latency_monitor ORDER BY hostA'):
    #     print(row)

    # print("*****************************************************************")

    # for row in cur.execute('SELECT * FROM bw ORDER BY hostA'):
    #     print(row)

    # print("*****************************************************************")

    # for row in cur.execute('SELECT * FROM bw_monitor ORDER BY hostA'):
    #     print(row)
